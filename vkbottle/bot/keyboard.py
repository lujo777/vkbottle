"""
 MIT License

 Copyright (c) 2019 Arseniy Timonik

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

from vkbottle.vkbottle.jsontype import dumps
from enum import Enum
from ..vk.exceptions import *
import six
from ..utils import Logger


def keyboard_generator(pattern, one_time=False):
    """Simple keyboard constructor
    :param pattern: Keyboard simple pattern, check github readme
    :param one_time: Should keyboard be hidden after first use?
    :return: VK Api Keyboard JSON
    """
    rows = pattern
    buttons = list()
    for row in rows:
        row_buttons = list()
        for button in row:
            row_buttons.append(dict(
                action=dict(
                    type="text" if 'type' not in button else button['type'],
                    label=button['text'],
                    payload=dumps("" if 'payload' not in button else button['payload'])
                ),
                color="default" if 'color' not in button else button['color']
            )
            )
        buttons.append(row_buttons)

    keyboard = str(dumps(
        dict(
            one_time=one_time,
            buttons=buttons
        ),
        ensure_ascii=False
    ).encode('utf-8').decode('utf-8'))

    return keyboard
