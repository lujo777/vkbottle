import asyncio
#from aiohttp_requests import requests

from random import randint
from ..utils import Utils
from ..events import Events
import requests
from ..jsontype import json_type_utils
from ..keyboard import _keyboard


# The main
class Bot(Events):
    def __init__(self, token, group_id, debug=False):
        __api_version__ = 5.101
        self.group_id = group_id
        self.token = token
        self.__debug = debug
        self.__utils = Utils(debug)
        self.__utils('Bot was authorised successfully')
        self.url = 'https://api.vk.com/method/'
        self.API_VERSION = __api_version__

    def method(self, method, args):
        res = requests.post(f'{self.url}{method}/?access_token={self.token}&v={self.API_VERSION}', data=args).json()
        return res

    async def async_method(self, method, args):
        res = await requests.post(f'{self.url}{method}/?access_token={self.token}&v={self.API_VERSION}', data=args).json()
        return res

    def run(self, wait=15):

        self.__utils('Found {} message decorators'.format(len(self._processor_message.keys())))
        self.__utils(json_type_utils())
        longpoll = self.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        longpoll = longpoll['response']
        ts = longpoll['ts']
        self.__utils('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                if event['updates']:
                    loop = asyncio.get_event_loop()
                    obj = event['updates'][0]['object']
                    if event['updates'][0]['type'] == 'message_new':
                        loop.run_until_complete(self.process_message(obj['text'], obj))
                    elif event['updates'][0]['type'] in self._events:
                        loop.run_until_complete(self.process_event(event))
            except requests.ConnectTimeout:
                self.__utils.warn('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                self.__utils.warn('ERROR! ' + str(e))
            try:
                longpoll = self.method(
                    'groups.getLongPollServer',
                    {"group_id": self.group_id}
                    )
                longpoll = longpoll['response']
                ts = longpoll['ts']
            except Exception as E:
                self.__utils.warn('LONGPOLL CONNECTION ERROR! ' + str(E))

    async def process_message(self, text: str, obj):
        answer = AnswerObject(self, obj)
        self.__utils('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self._processor_message:
            await self._processor_message[text](answer)
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
            await self._undefined_message_func(answer)

    async def process_event(self, event):
        self.__utils('\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(event['updates'][0]['object']['user_id'], event['updates'][0]['type']))
        event_compile = True
        for rule in self._events[event['updates'][0]['type']]['rule']:
            event_compile = False if event['updates'][0]['object'].get(rule[0], 'undefined') != rule[1] else True
        if event_compile:
            answer = AnswerObject(self, event['updates'][0]['object'])
            self.__utils('* EVENT RULES => TRUE. COMPILING EVENT')
            await self._events[event['updates'][0]['type']]['call'](answer)


class AnswerObject:
    def __init__(self, bot: Bot, obj):
        self.bot = bot
        self.obj = obj
        self.peer_id = obj["peer_id"] if 'peer_id' in obj else obj['user_id']
        self.group_id = bot.group_id

    def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                 chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None, payload=None,
                 dont_parse_links=False, disable_mentions=False):
        params = dict(
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
        request = {k: v for k, v in params.items() if v is not None}
        return Bot.method(self.bot, 'messages.send', args=request)
