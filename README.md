# ⚡ Cashu Monopoly 🎩

**Play Monopoly with your friends and family using real Bitcoin (ecash) or test tokens!**

This project transforms the classic board game into a Bitcoin experience. It uses the [Cashu](https://github.com/cashubtc) protocol to handle game funds, allowing players to buy in using a Lightning wallet, play the game, and cash out the pot at the end.


---

## 🎮 Try it Live!

Don't want to install anything? You can try the game right now on our test server:

👉 **[Play Cashu Monopoly](https://cashu-monopoly.onrender.com/)**

*Tip: Select "TestNut (Testnet)" in the game setup to play for free without spending real Bitcoin.*

---

## 👨‍👩‍👧‍👦 Why Play This?

This project is designed as a fun, interactive educational tool.

*   **Financial Literacy:** Teach children (and adults!) how to handle money, calculate inflows and outflows, and manage assets.
*   **Bitcoin Education:** It is the perfect safe sandbox to introduce friends and family to **Bitcoin, Lightning, and Ecash**.
*   **Micro-Stakes:** You can play with tiny amounts (e.g., 500 sats, which is a fraction of a Dollar). This makes the game feel "real" and exciting without huge financial risk.
*   **Math Skills:** The game dynamically scales prices based on your buy-in. If you buy in with 3000 sats, all rents, salaries, and fines double automatically!

---

## ✨ Features

*   **Mint Agnostic:** Connect to any Cashu Mint (Minibits, TestNut, or your own local Docker mint).
*   **Dynamic Scaling:** The game math adjusts automatically. Play a "High Roller" game with 1,000,000 sats or a "Micro" game with 500 sats.
*   **Automatic Invoices:** Generates Lightning invoices (BOLT11) for buy-ins.
*   **Instant Settlement:** The game server manages the pot using a custodial Cashu wallet for speed and ease of use.
*   **Cash Out:** At the end of the game, the winner receives a Cashu token containing the entire pot. Redeem it using your Cashu wallet of choice (e.g. [Cashu.me](https://wallet.cashu.me/))
*   **Offline Mode:** Play offline by installing the app as a PWA directly from your browser.

---

## 🛠️ Roadmap & Future Improvements

This project is a work in progress. Here is what is coming next:

### 🔒 Security & Persistence
*   **Server Persistence:** Currently, if the server restarts, the pot is lost. We need to implement database persistence so games can resume after a crash.
*   **Non-Custodial Options:** Ideally, the browser should hold the keys rather than the server, allowing strangers to play trustlessly over the internet in some future versions.

### 💸 Game Economy
*   **Partial Withdrawals:** Enable players to "cash out" their remaining share of the pot if they or the group decides to stop playing early.

### 📱 UI/UX
*   **Mobile Optimization:** The current board is best viewed on a desktop. We want to make it playable on mobile phones.
*   **Sound Effects:** Maybe add "Cha-ching!" sounds when rent is paid.
*   **Better QR Codes:** Make QR codes clickable on mobile to open wallets directly.

---

## 🚀 How to Run Locally

If you want to host your own game server or develop features:

### Prerequisites
*   Python 3.10+

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/bTCpy/monopoly.git
    cd monopoly
    ```

3. **Create a virtual environment**  
   Install [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) or use the build in python [venvs](https://docs.python.org/3/library/venv.html).
   ```bash
    conda create -n myvirtualenv python=3.13
    conda activate myvirtualenv
    ```

2.  **Install Dependencies**  
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Server**
    ```bash
    python main.py
    ```

5.  **Play**  
    Open your browser and navigate to `http://localhost:5000` respectively `http://127.0.0.1:5000/`.

---

## ⚠️ Disclaimer

**This software is in BETA.**
The game server currently acts as a custodian of the funds during the game. If the server crashes or the database is deleted, **funds may be lost.**

*   **Do not** play with amounts you cannot afford to lose.
*   **Do not** use this for high-stakes gambling.
*   Use the "TestNut" mint for risk-free testing.

---

## ❤️ Credits

*   **Game Logic & UI:** [Daniel Moyer (intrepidcoder)](https://github.com/intrepidcoder/monopoly)
*   **Ecash Protocol:** [Cashu](https://cashu.space)
