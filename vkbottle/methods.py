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
VK API WRAPPER
"""

import requests
from .vk.exceptions import *


class Api(object):
    def __init__(self, token, url, api_version, method=None):
        self.__token = token
        self.__url = url
        self.__api_version = api_version
        self._method = method

    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return Api(
            self.__token,
            self.__url,
            self.__api_version,
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, **kwargs):
        for k, v in enumerate(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)
        method = self._method.split('.')
        if len(method) == 2:
            group = method[0]
            method = method[1]

            return Method(self.__token, self.__url, self.__api_version)(group, method, kwargs)


class Method:
    def __init__(self, token, url, api_version):
        self.token = token
        self.url = url
        self.api_version = api_version

    def __call__(self, group, method, args):
        res = requests.post(
            f'{self.url}{group}.{method}/?access_token={self.token}&v={self.api_version}',
            data=args
        ).json()
        if 'response' not in res:
            """
            When the error appeared exception VKError will return list with error code and error message
            """
            raise VKError(
                [
                    res['error']['error_code'],
                    res['error']['error_msg']
                ]
            )
        else:
            return res['response']
