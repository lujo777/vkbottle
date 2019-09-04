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


from ...utils import make_priority_path

import re


def regex_message(text, formatted_pattern='{}'):
    escape = {ord(x): '\\' + x for x in r'\.*+?()[]|^$'}
    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(formatted_pattern.format(pattern))


class OnMessage(object):
    """
    OnMessage decorator wrapper. Needed for regex processing and advanced features support
    todo RU - покрасить забор
    """
    def __init__(self, events):
        self.processor = events.processor_message_regex

    def __call__(self, text: str, priority: int = 0):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, regex_message(text)],
                                                func)
            return func
        return decorator

    def startswith(self, text: str, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):

            pattern = regex_message(text, formatted_pattern='{}.*?')

            self.processor = make_priority_path(
                  self.processor,
                  *[priority, pattern],
                  func
            )

            return func

        return decorator

    def regex(self, pattern: str, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator


class OnMessageChat(object):
    """
    OnMessage in chat decorator wrapper. Needed for regex processing and advanced features support
    """
    def __init__(self, events):
        self.processor = events.processor_message_chat_regex

    def __call__(self, text: str, priority: int = 0):
        """
        Simple on.message_chat(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, regex_message(text)],
                                                func)
            return func
        return decorator

    def startswith(self, text: str, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message_chat.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern = regex_message(text, formatted_pattern='{}.*?')
            self.processor = make_priority_path(self.processor,
                                                *[priority, pattern],
                                                func)
            return func
        return decorator

    def regex(self, pattern: str, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator


class OnMessageBoth(object):
    """
    On private and in chat message decorator wrapper. Needed for regex processing and advanced features support
    """
    def __init__(self, events):
        self.processor_message = events.processor_message_regex
        self.processor_chat = events.processor_message_regex

    def __call__(self, text, priority: int = 0):
        """
        Simple on.message_both(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, regex_message(text)],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, regex_message(text)],
                                                     func)
            return func
        return decorator

    def startswith(self, text, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message_both.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern = regex_message(text, formatted_pattern='{}.*?')

            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, pattern],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, pattern],
                                                     func)
            return func
        return decorator

    def regex(self, pattern, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, re.compile(pattern)],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, re.compile(pattern)],
                                                     func)
            return func
        return decorator
