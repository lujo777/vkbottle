class Events:
    _processor_message = {}
    _processor_message_chat = {}
    _undefined_message_func = (lambda *args: print('Add to your on-message file an on-message-undefined decorator'))
    _events = {}

    def on_message(self, text):
        def decorator(func):
            self._processor_message[text] = func
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self._undefined_message_func = func
            return func
        return decorator

    def on_message_chat(self, text):
        def decorator(func):
            self._processor_message_chat[text] = func
            return func
        return decorator

    def on_group_join(self, join_type='join'):
        def decorator(func):
            self._events['group_join'] = {'call': func, 'rule': [['join_type', join_type]]}
            return func
        return decorator

    def on_group_leave(self, yourself=True):
        def decorator(func):
            self._events['group_leave'] = {'call': func, 'rule': [['self', int(yourself)]]}
            return func
        return decorator
