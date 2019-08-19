from .jsontype import json_type_utils

from .keyboard import _keyboard

from .methods import Method

from .path_loader import *

from random import randint

import re

import requests

import asyncio

import os


VERSION_PORTABLE = 'https://raw.githubusercontent.com/timoniq/vkbottle/master/portable/PORTABLE.json'


def checkup_plugins(plugin_folder, utils: Utils):
    if not os.path.exists(plugin_folder):
        os.mkdir(plugin_folder)
        utils('Plugin Folder was created, PATH "{}"'.format(plugin_folder))


# Bot Universal Class
class RunBot:
    def __init__(self, bot, token, async_use=False):

        self._token = token
        self.bot = bot

        # Set the default plugin priority for __name__ == "__main__" bot run
        self.bot.on(0)

        self.url = 'https://api.vk.com/method/'
        self.async_use = async_use
        self.utils = Utils(self.bot.debug)

        # [Feature] Newest VKBottle version checkup
        # Added v0.19#master
        actual_portable = requests.get(VERSION_PORTABLE).json()
        if actual_portable['version'] != self.bot.version:
            self.utils(
                'Newer version of VKBottle available ({})! '
                'Install it using \x1b[93;1mpip install vkbottle --upgrade\x1b[0m'.format(
                    actual_portable['version']
                )
            )
        else:
            self.utils('You are using the newest version of VKBottle')

        self.utils('Bot <\x1b[35m{}\x1b[0m> was authorised successfully'.format(self.bot.group_id))

        # [Support] Plugin Support
        # Added v0.20#master
        checkup_plugins(self.bot.plugin_folder, self.utils)
        self.plugins = load_plugins(self.bot.plugin_folder, self.utils)

        self.utils(
            'Module completed. MODULE USING LONGPOLL VERSION {}'.format(
                self.bot.api_version
            )
            )

        # Deprecated names
        # Added v0.18#master
        if 'asyncio' in self.bot.deprecated:
            self.utils.warn('Name \'asyncio\' is now deprecated. Use name \'async_use\' and read the docs at')
        self.method = Method(token, self.url, self.bot.api_version)
        self._loop = asyncio.get_event_loop

    def run(self, wait):

        self.utils(
            'Found {} message decorators'.format(
                    len(self.bot.on.processor_message_regex.keys()) +
                    len(self.bot.on.processor_message_chat_regex.keys())
            ))
        self.utils(json_type_utils())

        # [Feature] If LongPoll is not enabled in the group it automatically stops
        # Added v0.19#master
        longPollEnabled = self.method('groups', 'getLongPollSettings', {'group_id': self.bot.group_id})['is_enabled']

        # [Feature] Update messages dictionaries
        # Added v0.20#master
        self.bot.on.get_message()
        self.bot.on.get_message_chat()

        # [Support] Plugin Support
        # Added v0.20#master
        self.utils('Merging plugins..')
        for plugin in self.plugins:
            self.bot.on.append_plugin(plugin)

        if longPollEnabled:

            try:

                longpoll = self.method(
                    'groups',
                    'getLongPollServer',
                    {"group_id": self.bot.group_id}
                )
                ts = longpoll['ts']

                self.utils('Started listening LongPoll... TS', ts)

                self.__run(wait, longpoll, ts)

            except requests.ConnectionError or requests.ConnectTimeout:
                self.utils.error('LongPoll Connection error! Check your internet connection and try again!')

        else:
            self.utils.error('LongPoll is not enabled in your group')

    def __run(self, wait, longpoll, ts):

        longPollRecycling = False

        while True:
            try:
                # [Feature] If LongPoll has a queue of the events after request error
                # Added v0.18#master
                if longPollRecycling:
                    self.utils('Sorting a queue of messages after LongPoll Request error...')
                    event_recycling = self.method(
                        'messages', 'getConversations',
                        {'offset': 0, 'count': 200, 'filter': 'unanswered'}
                    )

                    for message in event_recycling['items']:

                        # Event Processing
                        loop = self._loop()
                        loop.run_until_complete(self.event_processor(message['last_message']))

                    longPollRecycling = False
                    self.utils('Events was sorted successfully, sorted {} messages'.format(
                        event_recycling['count']
                    ))

                # LongPoll event by server post method
                url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
                    longpoll['server'],
                    longpoll['key'],
                    ts,
                    wait
                )
                event = requests.post(url).json()

                # Event Processing
                loop = self._loop()
                loop.run_until_complete(self.event_processor(event))
                # Time behind the next request with multiprocessing - 0.3 sec

            except requests.ConnectionError or requests.ConnectTimeout:
                # No internet connection
                self.utils.warn('Request Connect Timeout! Reloading LongPoll..')
                longPollRecycling = True  # [Feature] If LongPoll has a queue of the events after request error

            except RuntimeError as warn:
                self.utils.warn(
                    'ATTENTION! Warn ({}) is called often because you use async functions when \'async_use\' is False'
                    ' or upside down!'.format(
                        warn
                    )
                )

            try:
                # LongPoll server receiving
                longpoll = self.method(
                    'groups',
                    'getLongPollServer',
                    {"group_id": self.bot.group_id}
                )
                ts = longpoll['ts']

            except Exception as e:
                self.utils.warn('LONGPOLL CONNECTION ERROR! ' + str(e))
                longPollRecycling = True  # [Feature] If LongPoll has a queue of the events after request error

    async def event_processor(self, event):
        try:
            if event['updates']:
                # If updates more than one
                for update in event['updates']:
                    obj = update['object']

                    if update['type'] == 'message_new':

                        if obj['peer_id'] < 2e9:
                            # For private messages
                            await self.process_message(obj['text'], obj)
                        else:
                            # [Action Support] Actions in chat return to the @on_chat_action decorator
                            if 'action' in obj:
                                # For actions
                                await self.process_chat_action(obj)
                            else:
                                # For chat messages
                                await self.process_message_chat(obj['text'], obj)

                    elif update['type'] in self.bot.on.events:
                        # For main LongPoll events
                        await self.process_event(event)

        except RuntimeError as warn:
            self.utils.warn(
                'ATTENTION! Warn ({}) is called often because you use async functions when \'async_use\' is False'
                ' or upside down!'.format(
                    warn
                )
            )

    async def process_message_chat(self, text: str, obj):
        try:
            # Answer object for fast chat msg-parsing

            # [Feature] Async Answers
            # Added v0.19#master
            ansObject = SynchroAnswer
            if self.async_use:
                ansObject = AsyncAnswer

            answer = ansObject.AnswerObjectChat(self.method, obj, self.bot.group_id)
            found = False
            plugin_priorities = sorted(self.bot.on.processor_message_chat_regex.keys(), key=int, reverse=True)
            for plugin_priority in plugin_priorities:
                priorities = sorted(self.bot.on.processor_message_chat_regex[plugin_priority].keys(),
                                    key=int, reverse=True)
                for priority in priorities:

                    for key in self.bot.on.processor_message_chat_regex[plugin_priority][priority]:

                        if key.match(text) is not None:
                            found = True

                            self.utils(
                                '\x1b[31;1m-> MESSAGE FROM CHAT {} TEXT "{}" TIME #'.format(
                                    obj['peer_id'],
                                    obj['text']
                                ))

                            try:
                                # Try to run Events processor with passed arguments
                                if self.async_use:
                                    # [Feature] Async Use
                                    # Added v0.19#master
                                    asyncio.ensure_future(
                                        self.bot.on.processor_message_chat_regex[plugin_priority][priority][key](
                                            answer, **key.match(text).groupdict()
                                        )
                                    )
                                else:
                                    self.bot.on.processor_message_chat_regex[plugin_priority][priority][key](
                                        answer,
                                        **key.match(text).groupdict()
                                    )
                            except TypeError:
                                self.utils.error(
                                    'ADD TO {} FUNCTION REQUIRED ARGS'.format(
                                        self.bot.on.processor_message_chat_regex
                                        [plugin_priority][priority][key].__name__
                                    ))
                            finally:
                                self.utils(
                                    'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                                        self.bot.on.processor_message_chat_regex
                                        [plugin_priority][priority][key].__name__,
                                        obj['from_id']
                                    ))
                                break

                    if found:
                        break
                if found:
                    break

        except RuntimeError as warn:
            self.utils.warn(
                'ATTENTION! Warn ({}) is called often because you use async functions when \'async_use\' is False'
                ' or upside down!'.format(
                    warn
                )
            )

    async def process_message(self, text: str, obj):
        try:

            # Answer object for fast msg-parsing

            # [Feature] Async Answers
            # Added v0.19#master
            ansObject = SynchroAnswer
            if self.async_use:
                ansObject = AsyncAnswer

            answer = ansObject.AnswerObject(self.method, obj, self.bot.group_id)

            self.utils(
                '\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(
                    obj['peer_id'],
                    obj['text']
                ))

            found = False

            plugin_priorities = sorted(self.bot.on.processor_message_regex.keys(), key=int, reverse=True)

            for plugin_priority in plugin_priorities:

                priorities = sorted(self.bot.on.processor_message_regex[plugin_priority].keys(), key=int, reverse=True)

                for priority in priorities:

                    for key in self.bot.on.processor_message_regex[plugin_priority][priority]:

                        if key.match(text) is not None:
                            found = True

                            try:
                                # [Feature] Async Use
                                # Added v0.19#master
                                if self.async_use:
                                    asyncio.ensure_future(
                                        self.bot.on.processor_message_regex
                                        [plugin_priority][priority][key](
                                            answer,
                                            **key.match(text).groupdict()
                                        )
                                    )
                                else:
                                    self.bot.on.processor_message_regex[plugin_priority][priority][key](
                                        answer,
                                        **key.match(text).groupdict()
                                    )
                            except TypeError:
                                self.utils.error(
                                    'ADD TO {} FUNCTION REQUIRED ARGS'.format(
                                        self.bot.on.processor_message_regex[plugin_priority][priority][key].__name__
                                    )
                                )
                            finally:
                                self.utils(
                                    'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                                        self.bot.on.processor_message_regex[plugin_priority][priority][key].__name__,
                                        obj['peer_id']
                                    )
                                )
                                break

                    if found:
                        break

            if not found:
                if self.async_use:
                    if not self.bot.on.undefined_message_func.__name__ == '<lambda>':
                        asyncio.ensure_future(self.bot.on.undefined_message_func(answer))
                    else:
                        self.bot.on.undefined_message_func(answer)
                else:
                    self.bot.on.undefined_message_func(answer)


                self.utils(
                    'New message compile decorator was not found. ' +
                    'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                        obj['peer_id']
                    ))

        except TypeError as warn:
            self.utils.warn(
                'ATTENTION! Warn ({}) is called often because you use async functions when \'async_use\' is False'
                ' or upside down!'.format(
                    warn
                )
            )

    async def process_event(self, event):
        try:
            print(event)

            self.utils(
                '\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(
                    event['updates'][0]['object']['user_id'],
                    event['updates'][0]['type']
                ))
            event_type = event['updates'][0]['type']
            rule = self.bot.on.events[event_type]['rule']

            if rule != '=':
                event_compile = True \
                    if rule in event['updates'][0]['object'] \
                    and event['updates'][0]['object'][rule] in self.bot.on.events[event_type]['equal'] \
                    else False

                if event_compile:
                    # [Feature] Async Answers
                    # Added v0.19#master
                    ansObject = SynchroAnswer
                    if self.async_use:
                        ansObject = AsyncAnswer

                    answer = ansObject.AnswerObject(self.method, event['updates'][0]['object'], self.bot.group_id)

                    self.utils('* EVENT RULES => TRUE. COMPILING EVENT')
                    # [Feature] Async Use
                    # Added v0.19#master
                    if self.async_use:
                        asyncio.ensure_future(
                            self.bot.on.events[event_type]['equal'][event['updates'][0]['object'][rule]](answer)
                        )
                    else:
                        self.bot.on.events[event_type]['equal'][event['updates'][0]['object'][rule]](answer)
                else:
                    self.utils('* EVENT RULES => FALSE. IGNORE EVENT')
            else:
                # [Feature] Async Answers
                # Added v0.19#master
                ansObject = SynchroAnswer
                if self.async_use:
                    ansObject = AsyncAnswer

                answer = ansObject.AnswerObject(self.method, event['updates'][0]['object'], self.bot.group_id)

                self.utils('* EVENT RULES => TRUE. COMPILING EVENT')
                # [Feature] Async Use
                # Added v0.19#master
                if self.async_use:
                    asyncio.ensure_future(self.bot.on.events[event_type]['equal']['='](answer))
                else:
                    self.bot.on.events[event_type]['equal']['='](answer)

        except TypeError as warn:
            self.utils.warn(
                'ATTENTION! Warn ({}) is called often because you use async functions when \'async_use\' is False'
                ' or upside down!'.format(
                    warn
                )
            )

    async def process_chat_action(self, obj):
        action = obj['action']
        if action['type'] in self.bot.chat_action_types:

            self.utils(
                '\x1b[31;1m-> NEW EVENT FROM CHAT {} TYPE "{}" TIME #'.format(
                    obj['peer_id'],
                    action['type'].upper()
                ))

            # [Feature] Async Answers
            # Added v0.19#master
            ansObject = SynchroAnswer
            if self.async_use:
                ansObject = AsyncAnswer

            answer = ansObject.AnswerObjectChat(self.method, obj, self.bot.group_id)

            # [Feature] Async Use
            # Added v0.19#master
            if self.async_use:
                asyncio.ensure_future(self.bot.chat_action_types[action['type']]['call'](answer))
            else:
                self.bot.chat_action_types[action['type']]['call'](answer)

            self.utils(
                'NEW ON-CHAT-ACTION EVENT WAS COMPILED >> '
                'Compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self.bot.chat_action_types[action['type']]['call'].__name__,
                    obj['from_id']
                ))


class AsyncAnswer:

    class AnswerObject:

        def __init__(self, method, obj, group_id):
            self.method = method
            self.obj = obj
            self.group_id = group_id
            self.peer_id = obj['peer_id'] if 'peer_id' in obj else obj['user_id']
            self.user_id = self.peer_id
            self.message = obj['text'] if 'text' in obj else ''
            self.self_parse = dict(
                group_id=group_id,
                peer_id=self.peer_id
            )
            # Functions

        async def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                           chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None,
                           payload=None, dont_parse_links=False, disable_mentions=False):
            message = await self.parser(message)
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

        async def parser(self, message):
            user_parse = list(set(re.findall(r'{user:\w+}', message)))
            group_parse = list(set(re.findall(r'{group:\w+}', message)))
            self_parse = list(set(re.findall(r'{self:\w+}', message)))

            if user_parse:
                user = self.method('users', 'get', {'user_ids': self.peer_id})[0]

                for parser in user_parse:
                    message = message.replace(
                        parser, str(user.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if group_parse:
                group = self.method('groups', 'getById', {'group_id': self.group_id})[0]

                for parser in group_parse:
                    message = message.replace(
                        parser, str(group.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if self_parse:
                self_ = self.self_parse

                for parser in self_parse:
                    message = message.replace(
                        parser, str(self_.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            return message

    class AnswerObjectChat:

        def __init__(self, method, obj, group_id):
            self.method = method
            self.obj = obj
            self.group_id = group_id
            self.peer_id = obj['peer_id']
            self.user_id = obj['from_id']
            self.message = obj['text']
            self.self_parse = dict(
                group_id=group_id,
                user_id=self.user_id,
                peer_id=self.peer_id
            )

        async def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                           chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None,
                           payload=None, dont_parse_links=False, disable_mentions=False):
            message = await self.parser(message)
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

        async def parser(self, message):
            user_parse = list(set(re.findall(r'{user:\w+}', message)))
            group_parse = list(set(re.findall(r'{group:\w+}', message)))
            self_parse = list(set(re.findall(r'{self:\w+}', message)))

            if user_parse:
                user = self.method('users', 'get', {'user_ids': self.user_id})[0]

                for parser in user_parse:
                    message = message.replace(
                        parser, str(user.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if group_parse:
                group = self.method('groups', 'getById', {'group_id': self.group_id})[0]

                for parser in group_parse:
                    message = message.replace(
                        parser, str(group.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if self_parse:
                self_ = self.self_parse

                for parser in self_parse:
                    message = message.replace(
                        parser, str(self_.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            return message


class SynchroAnswer:

    class AnswerObject:

        def __init__(self, method, obj, group_id):
            self.method = method
            self.obj = obj
            self.group_id = group_id
            self.peer_id = obj['peer_id']
            self.user_id = self.peer_id
            self.message = obj['text']
            self.self_parse = dict(
                group_id=group_id,
                peer_id=self.peer_id
            )
            # Functions

        def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                     chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None,
                     payload=None, dont_parse_links=False, disable_mentions=False):
            message = self.parser(message)
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

        def parser(self, message):
            user_parse = list(set(re.findall(r'{user:\w+}', message)))
            group_parse = list(set(re.findall(r'{group:\w+}', message)))
            self_parse = list(set(re.findall(r'{self:\w+}', message)))

            if user_parse:
                user = self.method('users', 'get', {'user_ids': self.peer_id})[0]

                for parser in user_parse:
                    message = message.replace(
                        parser, str(user.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if group_parse:
                group = self.method('groups', 'getById', {'group_id': self.group_id})[0]

                for parser in group_parse:
                    message = message.replace(
                        parser, str(group.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if self_parse:
                self_ = self.self_parse

                for parser in self_parse:
                    message = message.replace(
                        parser, str(self_.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            return message

    class AnswerObjectChat:

        def __init__(self, method, obj, group_id):
            self.method = method
            self.obj = obj
            self.group_id = group_id
            self.message = obj['text']
            self.peer_id = obj['peer_id']
            self.user_id = obj['from_id']
            self.self_parse = dict(
                group_id=group_id,
                user_id=self.user_id,
                peer_id=self.peer_id
            )

        def __call__(self, message: str, attachment=None, keyboard=None, sticker_id=None,
                     chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None,
                     payload=None, dont_parse_links=False, disable_mentions=False):
            message = self.parser(message)
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

        def parser(self, message):
            user_parse = list(set(re.findall(r'{user:\w+}', message)))
            group_parse = list(set(re.findall(r'{group:\w+}', message)))
            self_parse = list(set(re.findall(r'{self:\w+}', message)))

            if user_parse:
                user = self.method('users', 'get', {'user_ids': self.user_id})[0]

                for parser in user_parse:
                    message = message.replace(
                        parser, str(user.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if group_parse:
                group = self.method('groups', 'getById', {'group_id': self.group_id})[0]

                for parser in group_parse:
                    message = message.replace(
                        parser, str(group.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            if self_parse:
                self_ = self.self_parse

                for parser in self_parse:
                    message = message.replace(
                        parser, str(self_.get(parser[parser.find(':') + 1: parser.find('}')], 'undefined')))

            return message
