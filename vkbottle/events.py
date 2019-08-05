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
