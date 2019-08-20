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


class Geo(object):
    type: str = None
    coordinates: dict = None
    place: dict = None


class MessageObject(object):
    id: int = None
    date: int = None
    peer_id: int = None
    from_id: int = None
    text: str = None
    random_id: int = None
    ref: str = None
    ref_source: str = None
    attachments: list = None
    important: bool = None
    geo = Geo
    payload: str = None
    fwd_messages: list = None
    reply_message: dict = None


class Message(MessageObject):
    def __call__(self, message, attachment: str = None, keyboard: list = None,
                 sticker_id: int = None, chat_id: int = None, user_ids: str = None,
                 lat: float = None, long: float = None, reply_to: int = None,
                 forward_messages: str = None, disable_mentions: int = None,
                 dont_parse_links: int = None, payload: str = None):
        pass
