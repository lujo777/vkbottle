"""
 MIT License

 Copyright (c) 2019 Arseniy Timonik

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""


from ...types.longpoll import EventTypes

from ...methods import Api

from ..events import Events

from ...utils import Logger, sorted_dict_keys

import time

from ...types import types

from ...collections import colored

from ..patcher import Patcher


class UpdatesProcessor(object):
    """
    Processor of VK API LongPoll events
    """
    on: Events
    logger: Logger
    api: Api
    a: float
    patcher: Patcher

    async def new_update(self, event: dict):
        """
        Process VK Event Object
        :param event: VK Server Event object
        """

        for update in event['updates']:

            obj = update['object']

            if await self.patcher.check_for_whitelist(obj):

                if update['type'] == EventTypes.MESSAGE_NEW:

                    if obj['peer_id'] < 2e9:
                        await self.new_message(obj)

                    else:
                        if not 'action' in obj:
                            await self.new_chat_message(obj)
                        else:
                            await self.new_chat_action(obj)

                else:
                    # If this is an event of the group
                    print('receive event')
                    pass

    async def new_message(self, obj: dict):
        """
        Private message processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        await self.logger(
            colored(
                '-> MESSAGE FROM {} TEXT "{}" TIME #'.format(
                    obj['peer_id'],
                    obj['text'].replace('\n', ' / ')
            ),
                'red'
            )
        )

        answer = types.Message(**obj, api=[self.api])
        found: bool = False

        for priority in await sorted_dict_keys(self.on.processor_message_regex):

            for key in self.on.processor_message_regex[priority]:

                if key.match(answer.text) is not None:
                    found = True
                    # [Feature] Async Use
                    # Added v0.19#master
                    await self.on.processor_message_regex[priority][key](
                        answer,
                        **key.match(answer.text).groupdict()
                    )

                    await self.logger(
                        'New message compiled with decorator <' +
                        colored(self.on.processor_message_regex[priority][key].__name__, 'magenta') +
                        '> (from: {})'.format(
                            answer.from_id
                        ),
                        '>>', round(time.time() - self.a, 5)
                    )

                    break

            if found:
                break

        if not found:
            await self.on.undefined_message_func(answer)

    async def new_chat_message(self, obj: dict):
        """
        Chat messages processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        await self.logger(
            colored(
                '-> MESSAGE FROM CHAT {} TEXT "{}" TIME #'.format(
                    obj['peer_id'],
                    obj['text'].replace('\n', ' ')
                ),
                'red'
            ))

        answer = types.Message(**obj, api=[self.api])
        found: bool = False

        for priority in await sorted_dict_keys(self.on.processor_message_chat_regex):

            for key in self.on.processor_message_chat_regex[priority]:

                if key.match(answer.text) is not None:
                    found = True
                    # [Feature] Async Use
                    # Added v0.19#master
                    await self.on.processor_message_chat_regex[priority][key](
                        answer,
                        **key.match(answer.text).groupdict()
                    )

                    await self.logger(
                        'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                            self.on.processor_message_chat_regex[priority][key].__name__,
                            answer.from_id
                        ),
                        '>>', round(time.time() - self.a, 5)
                    )

                    break

            if found:
                break

    async def new_event(self, event_type: str, obj: dict):
        """
        LongPoll Events Processor
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """
        pass

    async def new_chat_action(self, obj: dict):
        """
        Chat Action Processor
        :param obj:
        :return: VK Server Event Object
        """
        action = obj['action']

        await self.logger(
            colored(
                '-> ACTION FROM CHAT {} TYPE "{}" TIME #'.format(
                    obj['peer_id'],
                    action['type']
                ),
                'red'
            ))

        if action['type'] in self.on.chat_action_types:
            if {**action, **self.on.chat_action_types[action['type']]['rules']} == action:
                answer = types.Message(**obj, api=[self.api])
                await self.on.chat_action_types[action['type']]['call'](answer)

                await self.logger(
                    'New action compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                        self.on.chat_action_types[action['type']]['call'].__name__,
                        answer.from_id
                    ),
                    '>>', round(time.time() - self.a, 5)
                )
