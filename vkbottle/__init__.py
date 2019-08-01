import vk_api
import requests
import json
from random import randint


def _keyboard(self, pattern, one_time=False):
    rows = pattern
    row = rows[0]
    buttons = list()
    for row in rows:
        row_buttons = list()
        button = row[0]
        for button in row:
            row_buttons.append(dict(
                action=dict(
                    type="text" if 'type' not in button else button['type'],
                    label=button['text'],
                    payload=json.dumps("" if 'payload' not in button else button['payload'])
                ),
                color="default" if 'color' not in button else button['color']
            )
            )
        buttons.append(row_buttons)

    keyboard = str(json.dumps(
        dict(
            one_time=one_time,
            buttons=buttons
        ),
        ensure_ascii=False
    ).encode('utf-8').decode('utf-8'))

    return keyboard


class Bot:
    _processor = {}
    _undefined_func = (lambda *args: print('Add to your on-message file an on-message-undefined decorator'))

    def __init__(self, token, group_id, rps_delay=0, debug=False):
        self.session = vk_api.VkApi(token=token,)
        self.session._auth_token()
        self.session.RPS_DELAY = rps_delay
        self.group_id = group_id
        self.debug = debug

    def process_message(self, text: str, obj):
        answer = MessageAnswer(obj, self.session, self.group_id)
        if text in self._processor:
            self._processor[text](answer)
        else:
            self._undefined_func(answer)

    def on_message(self, text):
        def decorator(func):
            self._processor[text] = func
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self._undefined_func = func
            return func
        return decorator

    def run(self):
        longpoll = self.session.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        ts = longpoll['ts']
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait=15"
                event = requests.post(url).json()
                if event['updates']:
                    if event['updates'][0]['type'] == 'message_new':
                        obj = event['updates'][0]['object']
                        self.process_message(obj['text'], obj)
            except requests.ConnectTimeout:
                print('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                print(e)
            try:
                longpoll = self.session.method(
                    'groups.getLongPollServer',
                    {"group_id": self.group_id}
                    )
                ts = longpoll['ts']
            except Exception as E:
                print(str(E))

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response


class MessageAnswer:
    def __init__(self, obj, session: vk_api.VkApi, group_id):
        self.obj = obj
        self.peer_id = obj["peer_id"]
        self.attachment = obj["attachments"]
        self.fwd_message = obj["fwd_messages"]
        self.session = session
        self.group_id = group_id

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response

    def __call__(self, text, attachment=None, keyboard=None, sticker=None):
        request = dict(
            message=text,
            keyboard=keyboard,
            attachment=attachment,
            peer_id=self.peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = _keyboard(self, keyboard)
        return self.method('messages', 'send', request)

    def send(self, peer_id, text, attachment=None, keyboard=None, sticker=None):
        request = dict(
            message=text,
            keyboard=keyboard,
            attachment=attachment,
            peer_id=peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = _keyboard(self, keyboard)
        return self.method('messages', 'send', request)

