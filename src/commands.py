# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:49:46 2020
Version 1.2


"""
import logging
import os
import signal

from emoji import emojize
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, ParseMode, \
    ReplyKeyboardRemove

from keyboard import dice_keyboard, donate_keyboard
from matching import decrypt_echo, match_dice_pattern

# from time import sleep

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %('
                           'message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

stop_echo = False


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    chat_id = update.effective_chat.id
    username = str(update.message.from_user.first_name)
    print(chat_id)
    print(username)
    hi_message = "Hi, " + username + "! Use the custom keyboard to roll " \
                                     "your dices.\n" \
                                     "To roll your own custom dices, type " \
                                     "/roll <customRoll> " \
                                     "(e.g. /roll 3d6)."
    keyboard = dice_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text=hi_message,
                             reply_markup=reply_markup)
    print('Bot started with custom keyboard.')

    global stop_echo
    stop_echo = False


def helper(update, context):
    """Send a message when the command /help is issued."""
    username = str(update.message.from_user.first_name)

    hi = 'Hi there, ' + str(username) + "! I am @DiceDiesBot! "
    purpose = 'I simulate dice dies and coin tosses, which can be used ' \
              'for rol games or any other purposes.\n'
    available = '\n' + '<b>Available Commands</b>'  # + '\n'

    help_text = hi + purpose + available + '''
    /start - Gives a brief introduction and starts the custom 
             keyboard.
    /help - Displays detailed inf... well, you can see already.
    /roll <i>[custom_dice]</i> - Rolls a custom dice following the 
             format <i>XdY</i>, where Y > 1 (e.g. 1d6). No custom dice will
             roll a 2d6.
    /stop - Stops the bot and closes the custom keyboard.
    /donate - Keep the bot alive supporting the developer by donating via
            PayPal.
                     
                     \nBy using the custom keyboard, you can roll the most popular combination of dices, as well toss a coin.
                     
                     \nThe result of the die displays who made the die, showing the individual values of each dice as well as the sum of all of them. In case of tossing coins, the result will be either "Heads" or "Tails", but no total sum will be displayed, since it makes no real sense.
        
                    \nIn case your favourite choice is not a default in the custom keyboard, feel free to read about the /roll command!
                    
                    \nAny donations will be kindly appreciated and will be used to keep the server for @DiceDiesBot active!
        '''
    update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


def echo(update, context):
    """Echo the user message."""

    global stop_echo
    if not stop_echo:
        username = str(update.message.from_user.first_name)
        reply = update.message.text
        chat_id = update.effective_chat.id

        decrypt_echo(chat_id, context, reply, username)


def roll(update, context):

    global stop_echo
    if not stop_echo:
        username = str(update.message.from_user.first_name)
        print(username)

        reply = ' '.join(context.args).lower()
        reply = '2d6' if reply == '' else reply

        dice_pattern = '^[1-9][0-9]*d{1}[1-9][0-9]*$'
        answer = match_dice_pattern(dice_pattern, reply, username)

        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def stop(update, context):
    goodbye_text = emojize('DiceDiesBot rolled :game_die:1 :game_die:1 '
                           'and stopped working. Have fun! \N{dancer}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=goodbye_text,
                             reply_markup=ReplyKeyboardRemove())
    global stop_echo
    stop_echo = True
    print('Bot stopped.')
    ReplyKeyboardRemove(selective=True)
    print('Keyboard removed')


def killmeplease(update, context):
    username = str(update.message.from_user.first_name)
    goodbye_text = emojize('DiceDiesBot rolled :game_die:1 :game_die:1 '
                           'and got terminated.\n'
                           'Contact the developer to be able to use the bot '
                           'again.')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=goodbye_text)

    print('Bot has been killed by user ', username)
    os.kill(os.getpid(), signal.SIGINT)


def donate(update, context):
    keyboard = donate_keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply = 'How much do you want to donate?'

    update.message.reply_text(reply, reply_markup=reply_markup)
    print('Show donation question and options')


def trial(update, context):
    keyboard = donate_keyboard

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    query.edit_message_text(text='Selected option: {}'.format(query.data))


# def alarm(context):
#    """Send the alarm message."""
#    job = context.job
#    context.bot.send_message(job.context, text='Beep!')
#
# def set_timer(update, context):
#    """Add a job to the queue."""
#    chat_id = update.message.chat_id
#    try:
#        # args[0] should contain the time for the timer in seconds
#        due = int(context.args[0])
#        if due < 0:
#            update.message.reply_text('Sorry we can not go back to future!')
#            return
#
#        # Add job to queue and stop current one if there is a timer already
#        if 'job' in context.chat_data:
#            old_job = context.chat_data['job']
#            old_job.schedule_removal()
#        new_job = context.job_queue.run_once(alarm, due, context=chat_id)
#        context.chat_data['job'] = new_job
#
#        update.message.reply_text('Timer successfully set!')
#
#    except (IndexError, ValueError):
#        update.message.reply_text('Usage: /set <seconds>')
#
# def unset(update, context):
#    """Remove the job if the user changed their mind."""
#    if 'job' not in context.chat_data:
#        update.message.reply_text('You have no active timer')
#        return
#
#    job = context.chat_data['job']
#    job.schedule_removal()
#    del context.chat_data['job']
#
#    update.message.reply_text('Timer successfully unset!')
#
# def caps(update, context):
#    text_caps = ' '.join(context.args).upper()
#    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
