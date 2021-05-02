# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 16:18:07 2020
Version 1.2

"""
import re
from decimal import Decimal
from emoji import demojize

from roll_calc import calculate_result
from dicts import menu_to_dice


def remove_emoji(emoji, message):
    clean_message = message.replace(emoji, "")

    return clean_message


def match_exact_string(pattern, message):
    matched_string = re.match(pattern, message)
    return matched_string


def define_answer(matched_string, coin, username):
    wrong_format_message = 'Wrong format. The die must be a number, letter ' \
                           '\"d\" and number higher than 1 (e.g. /roll ' \
                           '4d7).\n' \
                           'If /roll does not receive a custom dice, it ' \
                           'will use 2d6 as default instead.'
    if not matched_string or matched_string.group().endswith("d1"):
        answer = wrong_format_message
        print('Wrong roll.')
    else:
        answer = calculate_result(matched_string.group(), coin)
        answer = str(username) + " rolled " + str(answer)
    return answer


def do_matching_process(pattern, reply, username):
    reply = menu_to_dice[reply]
    return match_dice_pattern(pattern, reply, username)


def match_dice_pattern(pattern, reply, username):
    coin = reply.endswith('d2')
    print("Coin? ", coin)
    matched_string = match_exact_string(pattern, reply)
    answer = define_answer(matched_string, coin, username)
    return answer


def match_pos_decimal_number(pattern, text):
    matched_string = re.match(pattern, text)
    number = Decimal(matched_string.replace(',', '.'))
    number = round(number, 2)

    return number


def decrypt_echo(chat_id, context, reply, username):
    try:
        reply = remove_emoji(":game_die:", demojize(reply))
        print("Tried decryption with a result of", reply)
        dice_pattern = '^[1-9][0-9]*d{1}[1-9][0-9]*$'
        answer = do_matching_process(dice_pattern, reply,
                                     username)

        if answer is not "":
            context.bot.send_message(chat_id=chat_id, text=answer)
    except:
        message = '\'' + reply + '\' is not a listed die. If the format is ' \
                                 'right, try using /roll ' + reply + ' instead.'
        print(message)