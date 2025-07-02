from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from bot_handler import handle_user_input
from llm_response import generate_confirmation_message

TOKEN = "7966731855:AAH_PNcL1I42tuB7vZfhC-hgJjK2OlLLWto"

NAME, EMAIL, PHONE = range(3)
user_data = {}

def start(update, context):
    update.message.reply_text("👋 Hello! What is your name?")
    return NAME

def get_name(update, context):
    user_data["name"] = update.message.text
    update.message.reply_text("📧 Please provide your email address.")
    return EMAIL

def get_email(update, context):
    user_data["email"] = update.message.text
    update.message.reply_text("📱 What is your phone number?")
    return PHONE

def get_phone(update, context):
    user_data["phone"] = update.message.text
    crm_result = handle_user_input(user_data["name"], user_data["email"], user_data["phone"])
    response_msg = generate_confirmation_message(user_data["name"], user_data["email"], user_data["phone"])

    for crm, result in crm_result.items():
        response_msg += f"\n✅ Lead sent to {crm.capitalize()}"

    update.message.reply_text(response_msg)
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("🚫 Cancelled.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, get_email)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    print("🤖 Telegram bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
