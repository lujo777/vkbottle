from .jsontype import json_type_utils
from .utils import Utils
from .keyboard import _keyboard
from .methods import Method
from random import randint
import requests
import asyncio


# Non-async Bot
class RunBot:
    def __init__(self, bot, token):
        self._token = token
        self.bot = bot
        self.url = 'https://api.vk.com/method/'
        self.utils = Utils(self.bot.debug)
        self.utils('Non-async module completed')
        self.method = Method(token, self.url, self.bot.api_version)

    def run(self, wait):
        self.utils('Found {} message decorators'.format(len(self.bot.processor_message.keys())))
        self.utils(json_type_utils())
        longpoll = self.method(
            'groups',
            'getLongPollServer',
            {"group_id": self.bot.group_id}
        )
        ts = longpoll['ts']
        self.utils('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                if event['updates']:
                    obj = event['updates'][0]['object']
                    if event['updates'][0]['type'] == 'message_new':
                        self.process_message(obj['text'], obj)
                    if event['updates'][0]['type'] in self.bot.events:
                        self.process_event(event)
            except requests.ConnectTimeout:
                self.utils.warn('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                self.utils.warn('ERROR! ' + str(e))
            try:
                longpoll = self.method(
                    'groups',
                    'getLongPollServer',
                    {"group_id": self.bot.group_id}
                )
                ts = longpoll['ts']
            except Exception as E:
                self.utils.warn('LONGPOLL CONNECTION ERROR! ' + str(E))

    def process_message(self, text: str, obj):
        answer = AnswerObject(self.method, obj)
        self.utils('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self.bot.processor_message:
            self.bot.processor_message[text](answer)
            self.utils(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self.bot.processor_message[text].__name__, obj['peer_id']
                ))
        else:
            self.utils(
                'New message compile decorator was not found. ' +
                'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                    obj['peer_id']
                ))
            self.bot.undefined_message_func(answer)

    def process_event(self, event):
        self.utils(
            '\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(
                event['updates'][0]['object']['user_id'],
                event['updates'][0]['type']
            ))
        event_compile = True
        for rule in self.bot.events[event['updates'][0]['type']]['rule']:
            event_compile = False if event['updates'][0]['object'].get(rule[0], 'undefined') != rule[1] else True
        if event_compile:
            answer = AnswerObject(self.method, event['updates'][0]['object'])
            self.utils('* EVENT RULES => TRUE. COMPILING EVENT')
            self.bot.events[event['updates'][0]['type']]['call'](answer)


class AnswerObject:
    def __init__(self, method, obj):
        self.method = method
        self.obj = obj
        self.peer_id = obj["peer_id"] if 'peer_id' in obj else obj['user_id']

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


# Async Bot
class RunBotAsync:
    def __init__(self, bot, token):
        self._token = token
        self.bot = bot
        self.url = 'https://api.vk.com/method/'
        self.utils = Utils(self.bot.debug)
        self.utils('Non-async module completed')
        self.method = Method(token, self.url, self.bot.api_version)

    def run(self, wait):
        self.utils('Found {} message decorators'.format(len(self.bot.processor_message.keys())))
        self.utils(json_type_utils())
        longpoll = self.method(
            'groups',
            'getLongPollServer',
            {"group_id": self.bot.group_id}
        )
        ts = longpoll['ts']
        self.utils('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                if event['updates']:
                    loop = asyncio.get_event_loop()
                    obj = event['updates'][0]['object']
                    if event['updates'][0]['type'] == 'message_new':
                        loop.run_until_complete(self.process_message(obj['text'], obj))
                    if event['updates'][0]['type'] in self.bot.events:
                        loop.run_until_complete(self.process_event(event))
            except requests.ConnectTimeout:
                self.utils.warn('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                self.utils.warn('ERROR! ' + str(e))
            try:
                longpoll = self.method(
                    'groups',
                    'getLongPollServer',
                    {"group_id": self.bot.group_id}
                )
                ts = longpoll['ts']
            except Exception as E:
                self.utils.warn('LONGPOLL CONNECTION ERROR! ' + str(E))

    async def process_message(self, text: str, obj):
        answer = AnswerObject(self.method, obj)
        self.utils('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self.bot.processor_message:
            await self.bot.processor_message[text](answer)
            self.utils(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self.bot.processor_message[text].__name__, obj['peer_id']
                ))
        else:
            self.utils(
                'New message compile decorator was not found. ' +
                'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                    obj['peer_id']
                ))
            await self.bot.undefined_message_func(answer)

    async def process_event(self, event):
        self.utils(
            '\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(
                event['updates'][0]['object']['user_id'],
                event['updates'][0]['type']
            ))
        event_compile = True
        for rule in self.bot.events[event['updates'][0]['type']]['rule']:
            event_compile = False if event['updates'][0]['object'].get(rule[0], 'undefined') != rule[1] else True
        if event_compile:
            answer = AnswerObject(self.method, event['updates'][0]['object'])
            self.utils('* EVENT RULES => TRUE. COMPILING EVENT')
            await self.bot.events[event['updates'][0]['type']]['call'](answer)