from telegram.ext import Updater, CommandHandler, MessageHandler, Application, ConversationHandler, ContextTypes
from telegram import ForceReply, Update
import openai
import os
from telegram.ext import filters

bot_token = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

def handle_message(update: Update, context):
    message_text = update.message.text
    response_text = generate_response(message_text)
    update.message.reply_text(response_text)

def generate_response(message_text):
    prompt = "Prompt: " + message_text + "\nModel: your-model-here\n\nResponse:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=102,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = response.choices[0].text.strip()
    return response_text


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
