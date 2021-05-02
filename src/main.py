# -*- coding: utf-8 -*-
"""


t.me/ricks_dice_roller_bot for Telegram.



"""
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters

import commands

TOKEN = ' !!!BOT_TOKEN!!! '

updater = Updater(TOKEN, use_context=True)


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("trial", commands.trial))
    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(CommandHandler('help', commands.helper))
    dp.add_handler(CommandHandler('stop', commands.stop))
    dp.add_handler(CommandHandler('roll', commands.roll))
    dp.add_handler(CommandHandler('donate', commands.donate))
    dp.add_handler(CommandHandler('killmeplease', commands.killmeplease))

    dp.add_handler(MessageHandler(Filters.text, commands.echo))
    dp.add_handler(CallbackQueryHandler(commands.button))
    #    dp.add_handler(CommandHandler("set", commands.set_timer,
    #                                  pass_args=True,
    #                                  pass_job_queue=True,
    #                                  pass_chat_data=True))
    #    dp.add_handler(CommandHandler("unset", commands.unset, \
    #                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(commands.error)

    # Start the Bot
    updater.start_polling()
    print('Bot woke up')

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
