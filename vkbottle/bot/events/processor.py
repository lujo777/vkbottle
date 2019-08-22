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

from ...types import message


class UpdatesProcessor(object):
    """
    Processor of VK API LongPoll events
    """
    on: Events
    logger: Logger
    api: Api
    a: float

    async def new_update(self, event: dict):
        """
        Process VK Event Object
        :param event:
        :return:
        """

        for update in event['updates']:

            obj = update['object']

            if update['type'] == EventTypes.MESSAGE_NEW:

                if obj['peer_id'] < 2e9:
                    await self.new_message(obj)

                else:
                    pass

            else:
                # If this is an event of the group
                print('receive event')
                pass

        # await self.api.request('messages', 'send',
        #                       {'message': 'a?', 'random_id': random.randint(-2e9, 2e9), 'peer_id': obj['peer_id']})

        print(round(time.time() - self.a, 5))

    async def new_message(self, obj: dict):

        await self.logger(
            '\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(
                obj['peer_id'],
                obj['text'].replace('\n', ' / ')
            ))

        answer = message.Message(**obj)
        found: bool = False

        for priority in await sorted_dict_keys(self.on.processor_message_regex):

            for key in self.on.processor_message_regex[priority]:

                if key.match(answer.text) is not None:
                    found = True
                    try:
                        # [Feature] Async Use
                        # Added v0.19#master
                        await self.on.processor_message_regex[priority][key](
                            answer,
                            **key.match(answer.text).groupdict()
                        )
                    except TypeError:
                        await self.logger.error(
                            'ADD TO {} FUNCTION REQUIRED ARGS'.format(
                                self.on.processor_message_regex[priority][key].__name__
                            )
                        )
                    finally:
                        await self.logger(
                            'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                                self.on.processor_message_regex[priority][key].__name__,
                                obj['peer_id']
                            )
                        )
                        break

            if found:
                break

        if not found:
            await self.on.undefined_message_func(answer)
