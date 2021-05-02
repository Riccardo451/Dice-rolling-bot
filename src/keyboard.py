# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:31:31 2020
Version 1.1

"""
from telegram import InlineKeyboardButton
from emoji import emojize

dice = ':game_die:'
coin = '\U0001fa99'

def emoj(emoji, text):
    final_text = emoji + text + emoji

    return emojize(final_text)


dice_keyboard = [
    [emoj(dice, 'Toss Coin'), emoj(dice, '1d4'), emoj(dice, '2d4')],
    [emoj(dice, '1d6'), emoj(dice, '2d6'), emoj(dice, '3d6')],
    [emoj(dice, '1d8'), emoj(dice, '1d10')],
    [emoj(dice, '1d12'), emoj(dice, '1d20')]
]


def paypal(amount):
    link = 'https://www.paypal.me/'
    callback = amount

    if amount.isdigit():
        link = link + amount
        amount = str(amount) + '€'

    option = InlineKeyboardButton(amount, url=link + 'EUR',
                                  callback_data=callback)

    return option


donate_keyboard = [
    [paypal('5'), paypal('10'), paypal('20')],
    [paypal('Different Amount')]
]
