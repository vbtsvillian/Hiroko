import logging
import random
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Define your bot token
TOKEN = "YOUR_BOT_TOKEN"

# Define the API endpoint to fetch waifu images
API_ENDPOINT = "https://api.waifu.pics/sfw/waifu"

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text("Hello! I'm your Waifu Character Grab Bot. Use the /waifu command to get a random waifu character image!")

def waifu(update: Update, context: CallbackContext) -> None:
    """Grab and send a random waifu character image."""
    try:
        response = requests.get(API_ENDPOINT)
        if response.status_code == 200:
            data = response.json()
            image_url = data['url']
            update.message.reply_photo(photo=image_url)
        else:
            update.message.reply_text("Oops! Something went wrong. Please try again later.")
    except Exception as e:
        logger.error(str(e))
        update.message.reply_text("Oops! Something went wrong. Please try again later.")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("waifu", waifu))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
