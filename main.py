import asyncio
import os
import shutil
import gc  # Garbage Collector
from quart import Quart, jsonify, request, send_from_directory

# --- CONFIGURATION ---
os.environ["TOR"] = "FALSE"
os.environ["LIGHTNING"] = "FALSE"
os.environ["MINT_HOST"] = "localhost"
os.environ["MINT_PORT"] = "3338"
# Prevent library from reading a cached .env file
os.environ["CASHU_DIR"] = ".cashu_tmp"

# --- CASHU IMPORTS ---
from cashu.core.db import Database
from cashu.core.migrations import migrate_databases
from cashu.wallet import migrations
from cashu.wallet.wallet import Wallet
from cashu.core.base import Proof

TARGET_MINT_URL = "https://testnut.cashu.space" #"http://localhost:3338"
DB_DIR = "game_db"  # Back to a single, disposable directory

app = Quart(__name__, static_folder='.')

# Global State
wallet = None
game_pot = []
invoice_id = None
DEMO_MODE_ACTIVE = False
current_invoice_amount = 0
active_keyset_id = None

# --- HELPER: Aggressive Cleanup ---
async def nuke_and_reset_db():
    print("💥 NUKING DATABASE...")
    # 1. Force Python to release memory references
    global wallet
    wallet = None
    gc.collect() 
    
    # 2. Delete the directory
    if os.path.exists(DB_DIR):
        try:
            shutil.rmtree(DB_DIR)
            await asyncio.sleep(0.2) # Wait for OS
        except Exception as e:
            print(f"⚠️ Clean error: {e}")

    # 3. Re-create tables
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        temp_db = Database("wallet", DB_DIR)
        await migrate_databases(temp_db, migrations)
        print("✅ Database reset complete.")
    except Exception as e:
        print(f"❌ DB Reset Failed: {e}")

@app.before_serving
async def startup():
    global wallet
    print("\n--- 🚀 STARTING CASHU MONOPOLY ---")
    
    # Reset DB on startup
    await nuke_and_reset_db()

    # Init Default Wallet
    print(f"🔌 Connecting to default: {TARGET_MINT_URL}")
    try:
        wallet = Wallet(url=TARGET_MINT_URL, db=DB_DIR)
        await wallet.load_mint()
        await wallet.load_proofs(reload=True)
        if not hasattr(wallet, 'bip32'):
            await wallet._init_private_key(None)
        print("✅ Ready.")
    except Exception as e:
        print(f"⚠️ Default connection failed (OK): {e}")

@app.route('/')
async def index():
    return await send_from_directory('.', 'index.html')

@app.route('/<path:path>')
async def serve_static(path):
    return await send_from_directory('.', path)

@app.route('/api/debug_skip', methods=['POST'])
async def debug_skip():
    global DEMO_MODE_ACTIVE, game_pot
    print("⚠️ DEMO MODE: Skipping payment check...")
    DEMO_MODE_ACTIVE = True
    fake_proof = Proof(id="demo", amount=1000, secret="demo", C="02"+"00"*32)
    game_pot.append(fake_proof)
    return jsonify({"status": "skipped"})

@app.route('/api/buyin', methods=['POST'])
async def buyin():
    global invoice_id, DEMO_MODE_ACTIVE, current_invoice_amount, wallet, active_keyset_id
    DEMO_MODE_ACTIVE = False
    game_pot.clear()
    
    # 1. Get Data
    data = await request.get_json()
    amount_to_charge = int(data.get('amount', 1000))
    requested_mint_url = data.get('mint_url')
    current_invoice_amount = amount_to_charge

    # 2. HANDLE MINT SWITCHING
    current_url = wallet.url.rstrip('/') if wallet else ""
    req_url = (requested_mint_url or TARGET_MINT_URL).rstrip('/')

    # Always reset if the URL is different, OR if we just want to be safe
    if not wallet or req_url != current_url:
        print(f"🔄 SWITCHING MINT: {current_url} -> {req_url}")
        
        # A. NUKE EVERYTHING
        await nuke_and_reset_db()
        
        try:
            # B. CREATE NEW WALLET INSTANCE
            # We explicitly pass the url to ensure it doesn't use env vars
            new_wallet = Wallet(url=req_url, db=DB_DIR)
            
            # C. FORCE CLEAR INTERNAL STATE (Fix for Memory Pollution)
            new_wallet.keysets = {} 
            
            # D. LOAD MINT
            await new_wallet.load_mint()
            
            # E. SELECT KEYSET
            print(f"🔎 DEBUG: Scanning {len(new_wallet.keysets)} keysets...")
            target_id = None
            for k_id, k in new_wallet.keysets.items():
                unit_str = str(k.unit).lower()
                if unit_str == 'sat' or unit_str == 'sats':
                    if k.active:
                        target_id = k.id
                    elif target_id is None:
                        target_id = k.id
            
            if target_id:
                active_keyset_id = target_id
                new_wallet.keyset_id = target_id 
                print(f"🔑 Selected Keyset ID: {active_keyset_id}")
            else:
                print("❌ CRITICAL: No 'sat' keyset found!")
                active_keyset_id = None

            # F. INIT KEYS
            await new_wallet.load_proofs(reload=True)
            if not hasattr(new_wallet, 'bip32'):
                print("🔑 Generating new keys...")
                await new_wallet._init_private_key(None)

            wallet = new_wallet
            print(f"✅ Switched successfully to {req_url}")
            
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            return jsonify({"error": str(e)}), 500
    
    # 3. GENERATE INVOICE
    try:
        print(f"-> Invoice: {amount_to_charge} sats on {wallet.url}")
        mint_quote = await wallet.request_mint(amount_to_charge)
        invoice_id = mint_quote.quote 
        bolt11_str = mint_quote.request
        return jsonify({"payment_request": bolt11_str, "hash": invoice_id})
        
    except Exception as e:
        print(f"Error requesting mint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/check_start', methods=['POST'])
async def check_start():
    global game_pot, current_invoice_amount, active_keyset_id
    
    if DEMO_MODE_ACTIVE:
        return jsonify({"status": "paid", "pot_size": current_invoice_amount})

    if not invoice_id:
        return jsonify({"status": "waiting"})

    try:
        proofs = await wallet.mint(amount=current_invoice_amount, quote_id=invoice_id)
        game_pot.extend(proofs)
        total = sum(p.amount for p in game_pot)
        print(f"💰 PAID! Pot Size: {total} sats")
        return jsonify({"status": "paid", "pot_size": total})
        
    except Exception as e:
        # Suppress standard waiting errors
        if "paid" not in str(e) and "None" not in str(e): 
            print(f"⚠️ MINTING ERROR: {e}")
        return jsonify({"status": "waiting"})

@app.route('/api/cashout', methods=['POST'])
async def cashout():
    if not game_pot:
        return jsonify({"error": "Pot is empty"})
    
    try:
        token = await wallet.serialize_proofs(game_pot)
        game_pot.clear()
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
