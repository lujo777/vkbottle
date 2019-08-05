from .utils import Utils


class Events:
    processor_message = {}
    processor_message_chat = {}
    undefined_message_func = (
        lambda *args: Utils(True).warn('Add to your on-message file an on-message-undefined decorator')
    )
    events = {}

    def on_message(self, text):
        def decorator(func):
            self.processor_message[text] = func
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def on_message_chat(self, text):
        def decorator(func):
            self.processor_message_chat[text] = func
            return func
        return decorator

    def on_group_join(self, join_type='join'):
        def decorator(func):
            self.events['group_join'] = {'call': func, 'rule': [['join_type', join_type]]}
            return func
        return decorator

    def on_group_leave(self, yourself=True):
        def decorator(func):
            self.events['group_leave'] = {'call': func, 'rule': [['self', int(yourself)]]}
            return func
        return decorator
