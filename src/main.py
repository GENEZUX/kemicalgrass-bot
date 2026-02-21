import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from src.handlers.start import start
from src.handlers.terms import terms_handler

# Configuración básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_callback(update, context):
    \"\"\"Manejador global para botones inline.\"\"\"
    query = update.callback_query
    await query.answer()
    
    if query.data == \"legal_accept\":
        # Lógica para registrar aceptación
        from src.core.legal_checkpoint import LegalCheckpoint
        db = context.bot_data.get('db')
        checkpoint = LegalCheckpoint(db)
        await checkpoint.record_acceptance(update.effective_user.id, context.bot_data.get('tenant_id', 1), \"\")
        
        from src.handlers.start import show_main_menu
        await show_main_menu(update, context)
        
    elif query.data == \"legal_decline\":
        await query.edit_message_text(\"Lo sentimos, debe aceptar los términos para utilizar el bot.\")
    
    elif query.data == \"view_help\":
        await terms_handler(update, context)

def main():
    \"\"\"Función principal para iniciar el bot.\"\"\"
    token = os.getenv(\"TELEGRAM_TOKEN\")
    if not token:
        print(\"Error: TELEGRAM_TOKEN no configurado.\")
        return

    application = ApplicationBuilder().token(token).build()

    # Registro de handlers
    application.add_handler(CommandHandler(\"start\", start))
    application.add_handler(CommandHandler(\"terms\", terms_handler))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Iniciar bot (Polling para demo, Webhook para producción)
    print(\"KemicalGrass.BOT iniciado...\")
    application.run_polling()

if __name__ == '__main__':
    main()
