from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.core.legal_checkpoint import LegalCheckpoint

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"
    Handler para el comando /start.
    Implementa el checkpoint legal antes de mostrar el menú principal.
    \"\"\"
    user = update.effective_user
    tenant_id = context.bot_data.get('tenant_id', 1) # Default for SaaS demo
    db = context.bot_data.get('db')
    
    checkpoint = LegalCheckpoint(db)
    
    if await checkpoint.requires_acceptance(user.id, tenant_id):
        # Mostrar disclaimer legal
        keyboard = [
            [
                InlineKeyboardButton(\"✅ Acepto Términos\", callback_data=\"legal_accept\"),
                InlineKeyboardButton(\"❌ Rechazar\", callback_data=\"legal_decline\")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            checkpoint.get_legal_text(user.language_code),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # Si ya aceptó, mostrar menú principal
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(\"🏪 Catálogo\", callback_data=\"view_catalog\")],
        [InlineKeyboardButton(\"🛒 Mi Carrito\", callback_data=\"view_cart\")],
        [InlineKeyboardButton(\"📋 Mis Pedidos\", callback_data=\"view_orders\")],
        [InlineKeyboardButton(\"ℹ️ Ayuda y Términos\", callback_data=\"view_help\")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f\"🌿 **Bienvenido a KemicalGrass.BOT**\
\
Su plataforma segura para el comercio legal.\
¿Qué desea hacer hoy?\"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
