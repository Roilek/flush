# Create a telegram bot and host it on Heroku

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, Application, CallbackContext

import database

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

# Constants

TOKEN = os.environ.get('TOKEN')
PORT = int(os.getenv('PORT', 5000))
HEROKU_PATH = os.getenv('HEROKU_PATH')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.message.from_user.id
    text = ""
    if not database.user_exists(update.effective_user.id):
        database.register_user(user_id, update.effective_user.first_name, update.effective_user.last_name,
                               update.effective_user.username)
        text += "Welcome to Flush!\n"
    else:
        text += "Welcome back to Flush!\n"
    text += "You can try solving all the enigmas around FLEP. Just send me the enigma number and I'll send you the enigma\n"
    text += "Send me /help to see everything I can do!\n"
    await update.message.reply_text(text)
    return


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    text = "Here's everything I can do:\n"
    text += "/start - Start the bot\n"
    text += "/help - Show this message\n"
    # text += "/enigma - Get the enigma\n"
    # text += "/score - Get your score\n"
    # text += "/leaderboard - Get the leaderboard\n"
    # text += "/hint - Get a hint for the current enigma\n"
    # text += "/delete - Delete all your informations\n"
    # text += "/suggest - Suggest an enigma or a feature\n"
    # text += "/report - Report a bug\n"
    # text += "/contribute - Contribute to the bot\n"
    if database.is_admin(update.effective_user.id):
        text += "\nAdmin commands:\n"
        # text += "/add_enigma - Add an enigma\n"
        # text += "/delete_enigma - Delete an enigma\n"
        # text += "/add_hint - Add a hint\n"
        # text += "/delete_hint - Delete a hint\n"
        # text += "/add_admin - Add an admin\n"
        # text += "/delete_admin - Delete an admin\n"
    await update.message.reply_text(text)
    return


async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    return


async def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    return


def main() -> None:
    """Start the bot."""
    print("Going live!")

    # Create application
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    print("Bot starting...")
    if os.environ.get('ENV') == 'DEV':
        application.run_polling()
    elif os.environ.get('ENV') == 'PROD':
        application.run_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                webhook_url=HEROKU_PATH)
    return


if __name__ == '__main__':
    database.setup()
    main()
