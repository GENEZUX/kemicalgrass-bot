from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def view_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Muestra el catálogo de productos disponibles para el tenant.\"\"\"
    query = update.callback_query
    tenant_id = context.bot_data.get('tenant_id', 1)
    db = context.bot_data.get('db')
    
    # Mock de productos (esto vendría de la DB en prod)
    products = [
        {\"id\": 1, \"name\": \"Kemical Kush (Premium)\", \"price\": 2500, \"desc\": \"Alta potencia, aroma cítrico.\"},
        {\"id\": 2, \"name\": \"Grass Blue Dream\", \"price\": 1800, \"desc\": \"Equilibrado, ideal para el día.\"}
    ]
    
    text = \"🌿 **Catálogo de Productos Disponibles**\
\
\"
    keyboard = []
    for p in products:
        text += f\"🔹 **{p['name']}**\
💰 Price: ${p['price']/100:.2f}\
📝 {p['desc']}\
\
\"
        keyboard.append([InlineKeyboardButton(f\"🛒 Añadir {p['name']}\", callback_data=f\"add_to_cart_{p['id']}\")])
    
    keyboard.append([InlineKeyboardButton(\"🔙 Volver al Menú\", callback_data=\"main_menu\")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Handler para añadir productos al carrito (sesión en memoria/Redis).\"\"\"
    query = update.callback_query
    product_id = query.data.split('_')[-1]
    
    # Lógica simple de carrito en user_data
    if 'cart' not in context.user_data:
        context.user_data['cart'] = []
    
    context.user_data['cart'].append(product_id)
    
    await query.answer(text=\"✅ Producto añadido al carrito\")
