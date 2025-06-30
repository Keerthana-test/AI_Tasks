from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN
from session_manager1 import get_session, update_history, set_model, clear_session
from llm_gemini import query_gemini
from llm_ollama import query_ollama

# Show Gemini/Ollama selection when user starts
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Gemini", callback_data="use_gemini")],
        [InlineKeyboardButton("Ollama", callback_data="use_ollama")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🤖 Welcome! Choose a model to start chatting:", reply_markup=reply_markup)

# Handle model selection
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    model = "gemini" if query.data == "use_gemini" else "ollama"
    set_model(user_id, model)

    await query.edit_message_text(f"✅ Model selected: *{model.capitalize()}*\nNow send me a message!", parse_mode="Markdown")

# Reset command clears session
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_session(update.effective_user.id)
    await update.message.reply_text("🔄 Session has been reset. Use /start to begin again.")

# Handles messages based on selected model
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if not session["model"]:
        await update.message.reply_text("⚠️ Please select a model using /start before chatting.")
        return

    text = update.message.text
    full_history = update_history(user_id, f"User: {text}")

    if session["model"] == "gemini":
        reply = query_gemini(full_history)
    else:
        reply = query_ollama(full_history)

    update_history(user_id, f"Bot: {reply}")
    await update.message.reply_text(f"🤖 {reply}")

# App runner
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("✅ Bot running...")
    app.run_polling()
