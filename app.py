import os
import asyncio
import json
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from src.handlers.start import start
from src.handlers.terms import terms_handler

app = Flask(__name__)
_bot_app = None

async def build_application():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN not set")
    
    application = ApplicationBuilder().token(token).build()
    
    # Handlers from src/main.py
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("terms", terms_handler))
    
    # Import handle_callback dynamically
    from src.main import handle_callback
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    await application.initialize()
    return application

async def process_update(update_data):
    global _bot_app
    if not _bot_app:
        _bot_app = await build_application()
    
    update = Update.de_json(update_data, _bot_app.bot)
    await _bot_app.process_update(update)

@app.route('/webhook', methods=['POST'])
def webhook():
    update_data = request.get_json()
    if update_data:
        # Vercel supports asyncio in functions
        asyncio.run(process_update(update_data))
    return jsonify({"status": "ok"}), 200

@app.route('/')
def index():
    return "KemicalGrass.BOT Webhook is active.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
