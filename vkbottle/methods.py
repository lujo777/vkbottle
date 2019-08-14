from .keyboard import _keyboard
from random import randint
import requests
from .exceptions import *
import six


class Api(object):
    def __init__(self, token, url, api_version, method=None, user=False):
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
        for k, v in six.iteritems(kwargs):
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
