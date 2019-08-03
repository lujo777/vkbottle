import vk_api
import requests
from random import randint
from .utils import Utils
from .events import Events
from .jsontype import json_type_utils, dumps as json_dumps
from .methods import api
from .keyboard import _keyboard


# The main
class Bot(Events):
    def __init__(self, token, group_id, rps_delay=0, debug=False):
        self.__session = vk_api.VkApi(token=token)
        self.__session._auth_token()
        self.__session.RPS_DELAY = rps_delay
        self.group_id = group_id
        self.__debug = debug
        self.__utils = Utils(debug)
        self.__utils('Bot was authorised successfully')
        # Api Usage
        self.api = api(self.__session)

    def run(self, wait=15):
        self.__utils('Found {} message decorators'.format(len(self._processor_message.keys())))
        self.__utils(json_type_utils())
        longpoll = self.__session.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        ts = longpoll['ts']
        self.__utils('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                if event['updates']:
                    obj = event['updates'][0]['object']
                    if event['updates'][0]['type'] == 'message_new':
                        self.process_message(obj['text'], obj)
                    if event['updates'][0]['type'] in self._events:
                        self.process_event(event)
            except requests.ConnectTimeout:
                self.__utils.warn('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                self.__utils.warn('ERROR! ' + str(e))
            try:
                longpoll = self.__session.method(
                    'groups.getLongPollServer',
                    {"group_id": self.group_id}
                    )
                ts = longpoll['ts']
            except Exception as E:
                self.__utils.warn('LONGPOLL CONNECTION ERROR! ' + str(E))

    def process_message(self, text: str, obj):
        answer = AnswerObject(self, self.__session, obj)
        self.__utils('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self._processor_message:
            self._processor_message[text](answer)
            self.__utils(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self._processor_message[text].__name__, obj['peer_id']
                ))
        else:
            self.__utils(
                'New message compile decorator was not found. '\
                'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                    obj['peer_id']
                ))
            self._undefined_message_func(answer)

    def process_event(self, event):
        self.__utils('\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(event['updates'][0]['object']['user_id'], event['updates'][0]['type']))
        event_compile = True
        for rule in self._events[event['updates'][0]['type']]['rule']:
            event_compile = False if event['updates'][0]['object'].get(rule[0], 'undefined') != rule[1] else True
        if event_compile:
            answer = AnswerObject(self, self.__session, event['updates'][0]['object'])
            self.__utils('* EVENT RULES => TRUE. COMPILING EVENT')
            self._events[event['updates'][0]['type']]['call'](answer)

    def method(self, group, method, params):
        response = self.__session.method(f"{group}.{method}", params)
        return response


class AnswerObject:

    def __init__(self, bot: Bot, session, obj):
        self.bot = bot
        self.obj = obj
        self.peer_id = obj["peer_id"] if 'peer_id' in obj else obj['user_id']
        self.session = session
        self.group_id = bot.group_id

    def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                 chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None, payload=None,
                 dont_parse_links=False, disable_mentions=False):
        request = dict(
            message=message,
            keyboard=_keyboard(keyboard) if keyboard is not None else None,
            attachment=attachment,
            peer_id=self.peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker_id,
            chat_id=chat_id,
            user_ids=user_ids,
            lat=lat,
            long=long,
            reply_to=reply_to,
            forward_messages=forward_messages,
            payload=payload,
            dont_parse_links=dont_parse_links,
            disable_mentions=disable_mentions
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'send', request)

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response