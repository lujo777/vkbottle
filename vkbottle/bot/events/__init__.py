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

"""
VKBOTTLE EVENTS TYPES
"""

from ...utils import Logger, make_priority_path, dict_of_dicts_merge

from ...notifications import add_undefined

from .events import OnMessage, OnMessageChat, OnMessageBoth


class Events:
    def __init__(self, logger: Logger = Logger(True), use_regex: bool = True):
        """
        Make decorator processors (dictionaries with functions)
        :param logger: Logging object
        :param use_regex: More comfortable with regex, but if speed is main priority...
        fixme RU - не доделал это..
        """
        # Collections
        self.use_regex = use_regex

        # Processors
        self.processor_message_regex = {}

        self.processor_message_chat_regex = {}

        self.undefined_message_func = (lambda *args: logger.warn(add_undefined))

        self.events = {}

        self.chat_action_types = {}

        # Decorators
        self.message = OnMessage(self)

        self.message_chat = OnMessageChat(self)

        self.message_both = OnMessageBoth(self)

    def merge_processors(self):
        """
        Merge message decorators with message-both decorators. Using deepcopy and MutableMapping to merge dictionaries
        own priorities
        todo RU - исправить эту неприятную жижу
        """
        self.processor_message_regex = dict_of_dicts_merge(self.message.processor, self.message_both.processor_message)
        self.processor_message_chat_regex = dict_of_dicts_merge(self.message_chat.processor, self.message_both.processor_chat)

    def chat_action(self, type_: str):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        """
        def decorator(func):
            self.chat_action_types[type_] = {'call': func}
            return func
        return decorator

    def message_undefined(self):
        """
        If private message is not in message processor this single function will be caused
        """
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def event(self, name: str):
        """
        Event decorator. Needed for events processing.

        For example:
        @bot.on.event('on_group_join')
        :param name: Event name, find this in VK API Docs
        """
        def decorator(func):
            self.chat_action_types[name] = {'call': func}
            return func
        return decorator
