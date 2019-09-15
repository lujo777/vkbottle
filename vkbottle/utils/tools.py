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
VKBOTTLE WORK TOOLS
"""

from collections import MutableMapping
from aiohttp import ClientSession
from ..portable import VERSION_PORTABLE
from ..jsontype import json
import ssl


def dict_of_dicts_merge(d1, d2):
    """
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    """
    for k, v in d1.items():
        if k in d2:
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = dict_of_dicts_merge(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def make_priority_path(first: dict, priority, compile, second):
    """
    Make priority path for processors of Events class,
    [deprecated] [deprecated] [deprecated]
    fixme RU - убрать это нечто и перевести в мердж приоритетов
    """
    if priority not in first:
        first[priority] = {}
    if compile is not None:
        first[priority][compile] = second
    else:
        first[priority] = second
    return first


async def sorted_dict_keys(dictionary: dict, reverse=True):
    return sorted(list(dictionary.keys()), reverse=reverse)


def _request(func):
    """
    aioHTTP Request Decorator Wrapper
    :param func: wrapped function
    """
    async def decorator(*args, **kwargs):
        async with ClientSession(json_serialize=json.dumps) as client:
            funced = await func(*args, **kwargs, client=client)
        return funced
    return decorator


class HTTPRequest(object):
    """
    aioHTTP Request Wrapper
    """
    def __init__(self):
        self.client = ClientSession(json_serialize=json.dumps)

    @_request
    async def post(self, url, params: dict = None, client: ClientSession = None, content_type='application/json'):
        params = params or {}
        async with client.post(url, params=params, ssl=ssl.SSLContext()) as response:
            return await response.json(content_type=content_type)

    @_request
    async def get(self, url, client: ClientSession = None, content_type='application/json'):
        async with client.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json(content_type=content_type)


class HTTP(object):
    request = HTTPRequest()

