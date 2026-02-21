from telegram import Update
from telegram.ext import ContextTypes
from src.core.legal_checkpoint import LegalCheckpoint

async def terms_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Muestra los términos legales completos cuando el usuario lo solicita.\"\"\"
    user = update.effective_user
    db = context.bot_data.get('db')
    checkpoint = LegalCheckpoint(db)
    
    text = checkpoint.get_legal_text(user.language_code)
    # Aquí se podrían añadir más detalles de la política de privacidad
    await update.message.reply_text(text, parse_mode='Markdown')
