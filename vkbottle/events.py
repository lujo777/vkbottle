from .utils import Utils
import re


def regex_message(text):
    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text)
    return re.compile(pattern)


class Events:
    processor_message = {}
    processor_message_regex = {}
    processor_message_chat = {}
    processor_message_chat_regex = {}
    undefined_message_func = (
        lambda *args: Utils(True).warn('Add to your on-message file an on-message-undefined decorator')
    )
    events = {}

    def on_message(self, text):
        def decorator(func):
            items = re.findall(r'<\w+>', text)
            if len(items) == 0:
                self.processor_message[text] = {'call': func}
            else:
                self.processor_message_regex[regex_message(text)] = {'call': func}
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def on_message_chat(self, text):
        def decorator(func):
            items = re.findall(r'<\w+>', text)
            if len(items) == 0:
                self.processor_message_chat[text] = {'call': func}
            else:
                self.processor_message_chat_regex[regex_message(text)] = {'call': func}
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
