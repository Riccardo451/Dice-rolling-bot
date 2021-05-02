# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:43:28 2020
Version 1.2

"""
import re
from random import randint
from emoji import emojize

from dicts import int_to_happy, int_to_sad


def get_rolls(dice_roll, coin):
    print('Dice roll: ', dice_roll)
    number_rolls = int(re.match('^[0-9]+', dice_roll).group())
    print('Rolls: ', number_rolls)
    number_faces = int(dice_roll[re.match('^[0-9]+', dice_roll).end() + 1:])
    print('Faces: ', number_faces)
    result = []

    for rolls in range(number_rolls):
        result.append(randint(1, number_faces))

    return [result, number_rolls, number_faces]


def adapt_result(result, number_rolls, max_value, coin):
    result_size = len(result)
    adapted_result = ''
    current_sum = 0
    amount_max = 0
    amount_min = 0
    all_max = False
    all_min = False

    for i in range(result_size):
        separator = " "
        current_number = result.pop()
        [amount_max, amount_min] = same_value(amount_max, amount_min,
                                              current_number, max_value)
        current_sum = current_sum + current_number

        if coin:
            current_number = 'Tails' if current_number == 1 else 'Heads'

        adapted_result = adapted_result + separator + emojize(
            ':game_die:') + str(current_number)

    if number_rolls > 1:
        if amount_max == number_rolls:
            # happy ending
            all_max = True
        elif amount_min == number_rolls:
            # Sad ending
            all_min = True
    ending = add_ending_sum(result_size, current_sum, all_max, all_min, coin)

    return adapted_result + ending


def same_value(amount_max, amount_min, number, max_value):
    if number == max_value:
        amount_max = amount_max + 1
    elif number == 1:
        amount_min = amount_min + 1

    return [amount_max, amount_min]


def add_ending_sum(result_size, current_sum, all_max, all_min, coin):
    extra = ""
    ending = ". " if result_size == 1 or coin \
        else " = " + str(current_sum) + ". "

    if all_max:
        random_value = randint(1, len(int_to_happy))
        extra = int_to_happy[random_value]
    elif all_min:
        random_value = randint(1, len(int_to_sad))
        extra = int_to_sad[random_value]
    return ending + extra


def calculate_result(dice_roll, coin):
    [result, number_rolls, max_value] = get_rolls(dice_roll, coin)
    adapted_result = adapt_result(result, number_rolls, max_value, coin)

    return adapted_result
