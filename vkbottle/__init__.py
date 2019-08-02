import vk_api
import requests
import json
import ujson
import datetime
import re

from random import getrandbits, choice
from enum import Enum



class JSONType(Enum):
    STANDART = 'json'
    FAST = 'ujson'

class Bot:
    _processor = {}
    _undefined_func = (lambda *args: print('Add to your on-message file an on-message-undefined decorator'))

    def _keyboard(self, pattern, one_time=False):
        rows = pattern
        buttons = list()
        for row in rows:
            row_buttons = list()
            for button in row:
                if self.json_type == JSONType.STANDART:
                    row_buttons.append(dict(
                        action=dict(
                            type="text" if 'type' not in button else button['type'],
                            label=button['text'],
                            payload=json.dumps("" if 'payload' not in button else button['payload'])
                        ),
                        color="default" if 'color' not in button else button['color']
                    )
                    )
                else:
                    row_buttons.append(dict(
                        action=dict(
                            type="text" if 'type' not in button else button['type'],
                            label=button['text'],
                            payload=ujson.dumps("" if 'payload' not in button else button['payload'])
                        ),
                        color="default" if 'color' not in button else button['color']
                    )
                    )
            buttons.append(row_buttons)
        if self.json_type == JSONType.STANDART:
            keyboard = str(json.dumps(
                dict(
                    one_time=one_time,
                    buttons=buttons
                ),
                ensure_ascii=False
            ).encode('utf-8').decode('utf-8'))
        else:
            keyboard = str(ujson.dumps(
                dict(
                    one_time=one_time,
                    buttons=buttons
                ),
                ensure_ascii=False
            ).encode('utf-8').decode('utf-8'))

        return keyboard

    def log_debug(self, text):
        if self.debug is True:
            print("[\x1b[34mVK Bottle\x1b[0m] " + re.sub('#', str(datetime.datetime.now()), text) + "\x1b[0m")

    def __init__(self, token, group_id, json_type=JSONType.STANDART, rps_delay=0, debug=False):
        self.session = vk_api.VkApi(token=token)
        self.session._auth_token()
        self.session.RPS_DELAY = rps_delay
        self.json_type = json_type
        self.group_id = group_id
        self.debug = debug
        self.log_debug('Bot was authorised successfully')
        if json_type == JSONType.STANDART:
            self.log_debug('Using a standart(slow) method of json parsing.')
        if json_type == JSONType.FAST:
            self.log_debug('Using a fast method of json parsing.')

    def process_message(self, text: str, obj):
        answer = MessageAnswer(obj, self.session, self.group_id)
        self.log_debug('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self._processor:
            self._processor[text](answer)
            self.log_debug(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self._processor[text].__name__, obj['peer_id']
                ))
        else:
            self.log_debug(
                'New message compile decorator was not found. '\
                'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                    obj['peer_id']
                ))
            self._undefined_func(answer)

    def on_message(self, text):
        def decorator(func):
            self._processor[text] = func
            return func
        return decorator

    def onAddToChat(self, peer_id):
        def decorator(func):
            self._processor[peer_id] = func
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self._undefined_func = func
            return func
        return decorator

    event = ''  # plz don`t touch that

    def run(self, wait=15):
        self.log_debug('Found {} message decorators'.format(len(self._processor.keys())))
        longpoll = self.session.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        ts = longpoll['ts']
        self.log_debug('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                if event['updates']:
                    if event['updates'][0]['type'] == 'message_new':
                        obj = event['updates'][0]['object']
                        self.process_message(obj['text'], obj)
            except requests.ConnectTimeout:
                self.log_debug('Request Connect Timeout! Reloading longpoll..')
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
            random_id=getrandbits(31) * choice([-1, 1]),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = Bot._keyboard(self, keyboard)
        return self.method('messages', 'send', request)

    def send(self, peer_id, text, attachment=None, keyboard=None, sticker=None):
        request = dict(
            message=text,
            keyboard=keyboard,
            attachment=attachment,
            peer_id=peer_id,
            random_id=getrandbits(31) * choice([-1, 1]),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = Bot._keyboard(self, keyboard)
        return self.method('messages', 'send', request)

