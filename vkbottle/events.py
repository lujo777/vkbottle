from .utils import Utils
import re


def regex_message(text):
    escape = {ord(x): ('\\' + x) for x in r'\.*+?()[]|^$'}
    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(pattern)


class Events:
    processor_message_regex = {}
    processor_message_chat_regex = {}
    undefined_message_func = (
        lambda *args: Utils(True).warn('Add to your on-message file an on-message-undefined decorator')
    )
    events = {}
    chat_action_types = {}

    def on_message(self, text, priority: int = 0):
        def decorator(func):
            if priority not in self.processor_message_regex:
                self.processor_message_regex[priority] = {}
            self.processor_message_regex[priority][regex_message(text)] = {'call': func}
            return func
        return decorator

    def on_chat_action(self, type_):
        def decorator(func):
            self.chat_action_types[type_] = {'call': func}
            return func
        return decorator

    def on_message_both(self, text, priority: int = 0):
        def decorator(func):
            if priority not in self.processor_message_regex:
                self.processor_message_regex[priority] = {}
            if priority not in self.processor_message_chat_regex:
                self.processor_message_chat_regex[priority] = {}
            self.processor_message_regex[priority][regex_message(text)] = {'call': func}
            self.processor_message_chat_regex[priority][regex_message(text)] = {'call': func}
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def on_message_chat(self, text, priority: int = 0):
        def decorator(func):
            if priority not in self.processor_message_chat_regex:
                self.processor_message_chat_regex[priority] = {}
            self.processor_message_chat_regex[priority][regex_message(text)] = {'call': func}
            return func
        return decorator

    def on_group_join(self, join_type='join'):
        def decorator(func):
            if 'group_join' not in self.events:
                self.events['group_join'] = {'rule': 'join_type', 'equal': {join_type: func}}
            else:
                self.events['group_join']['equal'][join_type] = func
            return func
        return decorator

    def on_group_leave(self, yourself=True):
        def decorator(func):
            event = 'group_leave'
            if event not in self.events:
                self.events[event] = {'rule': 'self', 'equal': {yourself: func}}
            else:
                self.events[event]['equal'][yourself] = func
            return func
        return decorator

    def on_message_reply(self):
        def decorator(func):
            event = 'message_reply'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator

    def on_message_allow(self):
        def decorator(func):
            event = 'message_allow'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator

    def on_message_deny(self):
        def decorator(func):
            event = 'message_deny'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator

