from flask import Flask
import threading
import asyncio
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is Running! <a href='https://glitch.com/edit/#!/your-project-name'>Edit on Glitch</a>"

def run_flask():
    app.run(host='0.0.0.0', port=3000)

def run_telegram_bot():
    asyncio.run(run_bot())

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    run_telegram_bot()
