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

"""
VK API MESSAGE TYPES
"""


from pydantic import BaseModel

from random import randint


class Geo(object):
    type: str
    coordinates: dict
    place: dict


class Message(BaseModel):
    id: int
    date: int
    peer_id: int
    from_id: int
    text: str
    random_id: int
    ref: str = None
    ref_source: str = None
    attachments: list
    important: bool
    geo = Geo
    payload: str = None
    fwd_messages: list
    reply_message: dict = None
    api: list = None

    async def __call__(self, message: str = None, attachment: str = None, keyboard: list = None,
                 sticker_id: int = None, chat_id: int = None, user_ids: str = None,
                 lat: float = None, long: float = None, reply_to: int = None,
                 forward_messages: str = None, disable_mentions: int = None,
                 dont_parse_links: int = None, payload: str = None):
        return await self.api[0].request(
            'messages',
            'send',
            dict(
                peer_id=self.peer_id,
                random_id=randint(-1e9, 1e9),
                message=message,
                attachment=attachment,
                keyboard=keyboard,
                sticker_id=sticker_id,
                chat_id=chat_id,
                user_ids=user_ids,
                lat=lat,
                long=long,
                reply_to=reply_to,
                forward_messages=forward_messages,
                disable_mentions=disable_mentions,
                dont_parse_links=dont_parse_links,
                payload=payload
            )
        )

    async def reply(self, message: str = None, attachment: str = None, keyboard: list = None,
                 sticker_id: int = None, chat_id: int = None, user_ids: str = None,
                 lat: float = None, long: float = None, reply_to: int = None,
                 forward_messages: str = None, disable_mentions: int = None,
                 dont_parse_links: int = None, payload: str = None):
        return await self.api[0].request(
            'messages',
            'send',
            dict(
                peer_id=self.peer_id,
                random_id=randint(-1e9, 1e9),
                message=message,
                attachment=attachment,
                keyboard=keyboard,
                sticker_id=sticker_id,
                chat_id=chat_id,
                user_ids=user_ids,
                lat=lat,
                long=long,
                reply_to=reply_to or self.id,
                forward_messages=forward_messages,
                disable_mentions=disable_mentions,
                dont_parse_links=dont_parse_links,
                payload=payload
            )
        )
