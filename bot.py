from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import configs.config as config
import statistics


def start(bot, update):
    print_keyboard(update.message)


def print_keyboard(message):
    keyboard = [[InlineKeyboardButton("Day", callback_data='day'),
                 InlineKeyboardButton("Week", callback_data='week'),
                 InlineKeyboardButton("Month", callback_data='month')],
                [InlineKeyboardButton("All", callback_data='all')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message.reply_text('Please choose:', reply_markup=reply_markup)


def button_handler(bot, update):
    result = statistics.get_statistics(update.callback_query.data)

    message = update.callback_query.message

    bot.send_message(chat_id=message.chat_id,
                     text=result)

    print_keyboard(message)


def main():
    updater = Updater(config.get_telegram_token())

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    config.load()
    main()
