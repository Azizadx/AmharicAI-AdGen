from config import TELEGRAM_TOKEN
#  WebApp_URL

import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# url_web_app=WebApp_URL
token=TELEGRAM_TOKEN
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Click to open Web-App",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open AiQEM Web-App ",
                web_app=WebAppInfo(url="https://aqim-web-app.vercel.app"),
            )
        ),
    )
# Define a `/stop` command handler. 
def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop the bot."""
    update.message.reply_text('Bot stopped.')
    context.application.stop()



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()