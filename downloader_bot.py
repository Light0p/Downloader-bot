import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send me a link to download the file.")

# Function to download a file from a URL
def download_file(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an error for bad responses
        filename = url.split("/")[-1]
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return None

# Message handler for links
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    logger.info(f"Received URL: {url}")

    # Attempt to download the file
    filename = download_file(url)
    if filename:
        with open(filename, 'rb') as file:
            update.message.reply_document(file)
    else:
        update.message.reply_text("Failed to download the file. Please check the URL.")

# Main function to set up the bot
def main() -> None:
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    updater = Updater("7511374887:AAFrYbS9kE095NXVaq4lEyCSKHg0VBIM6r4")
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    