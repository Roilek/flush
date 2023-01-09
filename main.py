# Create a telegram bot and host it on Heroku

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, Application, CallbackContext, MessageHandler, filters

import database
from Enigma import Enigma

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

# Constants

TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT', 5000))
HEROKU_PATH = os.getenv('HEROKU_PATH')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    text = ""
    if not database.user_exists(user_id):
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
    text += "/reset - Reset your enigma\n"
    text += "/enigma - Get the enigma\n"
    text += "/score - Get your score\n"
    text += "/leaderboard - Get the leaderboard\n"
    text += "/hint - Get a hint for the current enigma\n"
    text += "/delete - Delete all your informations\n"
    text += "/suggest - Suggest an enigma or a feature\n"
    text += "/report - Report a bug\n"
    text += "/contribute - Contribute to the bot\n"
    if database.is_admin(update.effective_user.id):
        text += "\nAdmin commands:\n"
        text += "/add_enigma - Add an enigma\n"
        text += "/delete_enigma - Delete an enigma\n"
        text += "/add_hint - Add a hint\n"
        text += "/delete_hint - Delete a hint\n"
        text += "/add_admin - Add an admin\n"
        text += "/delete_admin - Delete an admin\n"
    await update.message.reply_text(text)
    return


async def reset(update: Update, context: CallbackContext) -> None:
    """Reset the user's enigma"""
    user_id = update.effective_user.id
    database.reset_user_enigma(user_id)
    await update.message.reply_text("You can send me a new enigma number to start guessing again!")
    return


async def report(update: Update, context: CallbackContext) -> None:
    """Report a bug"""
    await update.message.reply_text("Not implemented yet...")
    return


async def suggest(update: Update, context: CallbackContext) -> None:
    """Suggest an enigma or a feature"""
    await update.message.reply_text("Not implemented yet...")
    return


async def contribute(update: Update, context: CallbackContext) -> None:
    """Contribute to the bot"""
    await update.message.reply_text("Not implemented yet...")
    return


async def enigma(update: Update, context: CallbackContext) -> None:
    """Display the current enigma of the user"""
    await update.message.reply_text("Not implemented yet...")
    return


async def score(update: Update, context: CallbackContext) -> None:
    """Get the user's score"""
    await update.message.reply_text("Not implemented yet...")
    return


async def leaderboard(update: Update, context: CallbackContext) -> None:
    """Get the leaderboard"""
    await update.message.reply_text("Not implemented yet...")
    return


async def hint(update: Update, context: CallbackContext) -> None:
    """Get a hint for the current enigma"""
    await update.message.reply_text("Not implemented yet...")
    return


async def delete(update: Update, context: CallbackContext) -> None:
    """Delete all user's data"""
    await update.message.reply_text("Not implemented yet...")
    return


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle messages"""
    # The message text can be an enigma number or an enigma answer
    user_id = update.effective_user.id
    text = ""
    if database.user_has_enigma(user_id):
        # The user is attempting to solve an enigma
        enigma = database.get_user_enigma(user_id)
        enigma_id = enigma.get_id()
        enigma_solved = enigma.answer_is_correct(update.message.text)
        if enigma_solved:
            # The answer is correct
            # Update the user's enigma
            database.reset_user_enigma(user_id)
            text += "You solved the enigma!\n"
            text += "You can send me a new enigma id to try to solve another enigma\n"
        else:
            # The answer is incorrect
            text += f"The answer is incorrect for enigma {enigma_id}\n"
            text += "Try again or send /reset to be able to send a new enigma id"
        database.add_attempt(user_id, enigma_id, update.message.text, enigma_solved)
    else:
        # The user is sending an enigma id
        enigma_id = update.message.text
        # Check if the message is a number
        if not enigma_id.isdigit():
            text += "The enigma id must be a number\n"
        # Check if the enigma exists
        elif not database.enigma_exists(int(enigma_id)):
            # The enigma does not exist
            text += "This enigma doesn't exist! If you think this is a problem, please /report it!\n"
        else:
            # The enigma exists
            enigma_id = int(enigma_id)
            enigma = database.get_enigma(enigma_id)
            # Check if the user already solved this enigma
            if database.user_solved_enigma(user_id, enigma_id):
                text = "You already solved this enigma!\n"
                text += enigma.get_html_answer()
            else:
                # Update the user's enigma
                database.update_user_enigma(user_id, enigma_id)
                # Send the enigma
                text += enigma.get_html_enigma()
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return


async def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    return


# Admin commands


async def add_enigma(update: Update, context: CallbackContext) -> None:
    """Add an enigma"""
    if not database.is_admin(update.effective_user.id):
        await update.message.reply_text("You are not an admin!")
        return
    new_enigma = Enigma.from_str(update.message.text)
    if new_enigma is None:
        text = "The enigma is not valid!"
    else:
        database.add_enigma(new_enigma)
        text = "The enigma has been added!"
    await update.message.reply_text(text)
    return


async def delete_enigma(update: Update, context: CallbackContext) -> None:
    """Delete an enigma"""
    await update.message.reply_text("Not implemented yet...")
    return


async def add_hint(update: Update, context: CallbackContext) -> None:
    """Add a hint"""
    await update.message.reply_text("Not implemented yet...")
    return


async def delete_hint(update: Update, context: CallbackContext) -> None:
    """Delete a hint"""
    await update.message.reply_text("Not implemented yet...")
    return


async def add_admin(update: Update, context: CallbackContext) -> None:
    """Add an admin"""
    await update.message.reply_text("Not implemented yet...")
    return


async def delete_admin(update: Update, context: CallbackContext) -> None:
    """Delete an admin"""
    await update.message.reply_text("Not implemented yet...")
    return


def main() -> None:
    """Start the bot."""
    print("Going live!")

    # Create application
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("suggest", suggest))
    application.add_handler(CommandHandler("contribute", contribute))
    application.add_handler(CommandHandler("enigma", enigma))
    application.add_handler(CommandHandler("score", score))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("hint", hint))
    application.add_handler(CommandHandler("delete", delete))

    # Admin commands

    application.add_handler(CommandHandler("add_enigma", add_enigma))
    application.add_handler(CommandHandler("delete_enigma", delete_enigma))
    application.add_handler(CommandHandler("add_hint", add_hint))
    application.add_handler(CommandHandler("delete_hint", delete_hint))
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("delete_admin", delete_admin))

    # on noncommand i.e message - process the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

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
