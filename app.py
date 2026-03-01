from flask import Flask, request, redirect
import telebot
import random, string, json, time, os

BOT_TOKEN = os.environ.get("8763124556:AAE4tLkBEUFs_Dx-xewEAhbG5QNTjsenC3Y")
BOT_USERNAME = "Getcontent2026_bot"   # yaha apna bot username likho (without @)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

TOKEN_EXPIRY = 300  # 5 minutes

def load_tokens():
    try:
        with open("tokens.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_tokens(data):
    with open("tokens.json", "w") as f:
        json.dump(data, f)

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

@app.route("/")
def home():
    ref = request.headers.get("Referer")

    if not ref:
        return "Access Denied"

    token = generate_token()
    tokens = load_tokens()

    tokens[token] = {
        "time": time.time(),
        "used": False,
        "ip": request.remote_addr
    }

    save_tokens(tokens)

    return redirect(f"https://t.me/{BOT_USERNAME}?start={token}")

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()

    if len(args) > 1:
        user_token = args[1]
        tokens = load_tokens()

        if user_token in tokens:
            token_data = tokens[user_token]

            if token_data["used"]:
                bot.send_message(message.chat.id, "❌ Token already used.")
                return

            if time.time() - token_data["time"] > TOKEN_EXPIRY:
                bot.send_message(message.chat.id, "❌ Token expired.")
                return

            tokens[user_token]["used"] = True
            save_tokens(tokens)

            bot.send_message(message.chat.id, "✅ Verification Successful!")
            bot.send_document(message.chat.id, open("file.zip", "rb"))

        else:
            bot.send_message(message.chat.id, "❌ Invalid or Bypassed Link.")
    else:
        bot.send_message(message.chat.id, "Please complete the link properly.")

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=10000)
