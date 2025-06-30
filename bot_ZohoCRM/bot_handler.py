import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

from zoho_leads import search_lead_by_phone, create_lead
from llm_response import generate_response

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Step identifiers for conversation
ASK_NAME, ASK_EMAIL = range(2)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Please enter your phone number:")
    return ASK_NAME

# Step 1: Ask name if phone not found
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data["phone"] = phone

    lead = search_lead_by_phone(phone)
    if lead:
        name = lead.get("Last_Name", "there")
        context.user_data["lead_found"] = True
        await update.message.reply_text(f"👋 Hi {name}, how can I help you today?")
        return ConversationHandler.END
    else:
        context.user_data["lead_found"] = False
        await update.message.reply_text("🔍 I couldn't find your details. What's your name?")
        return ASK_EMAIL

# Step 2: Ask for email if name is entered
async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📧 Please enter your email address:")
    return ConversationHandler.END

# Handles all regular user messages after onboarding
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "lead_found" not in context.user_data:
        await update.message.reply_text("❗ Please type /start to begin.")
        return

    if not context.user_data.get("lead_found") and "email" not in context.user_data:
        context.user_data["email"] = text
        name = context.user_data["name"]
        phone = context.user_data["phone"]
        email = context.user_data["email"]

        result = create_lead(name, email, phone)
        if result:
            await update.message.reply_text("✅ You're registered! Ask me anything.")
        else:
            await update.message.reply_text("❌ Error saving your details. Try again.")
        return

    # LLM response
    reply = generate_response(text)
    await update.message.reply_text(reply)

# Reset command
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🔄 Session reset. Type /start to begin again.")

# Main bot function
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN missing in .env")
        return

    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
        },
        fallbacks=[CommandHandler("reset", reset)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
