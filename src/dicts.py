# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:47:38 2020
Version 1.2

"""
from emoji import emojize

int_to_happy = {
    1: 'Critical hit!',
    2: 'Smooth.',
    3: 'Awesome!',
    4: 'That\'s the way!',
    5: emojize(':four_leaf_clover:'),
    6: "What a roll!",
    7: '\N{dancer}',
    8: '\U0001F483\U0001F483\U0001F483'
}

int_to_sad = {
    1: 'You suck.',
    2: 'Try harder next time.',
    3: 'Ouch...',
    4: 'Pff, good luck...!',
    5: 'Loser.',
    6: "\U0001F4A9", # emojize(':trollface:'),
    7: 'Critical FAIL.'
}

menu_to_dice = {
    'Toss Coin': '1d2',
    '1d3': '1d3',
    '1d4': '1d4',
    '2d4': '2d4',
    '1d6': '1d6',
    '2d6': '2d6',
    '3d6': '3d6',
    '1d8': '1d8',
    '1d10': '1d10',
    '1d12': '1d12',
    '1d20': '1d20'
}
