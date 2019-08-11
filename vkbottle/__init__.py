from .utils import Utils

from .events import Events

from .jsontype import json_type_utils, dumps as json_dumps

from .methods import Api

from .keyboard import _keyboard

from .vkbottle import AnswerObject, RunBot

from .exceptions import *

__version__ = '0.11'  # Package VKBottle version

__api_version__ = 5.101  # VK Api version


# Main Bot Auth
class Bot(Events):
    def __init__(self, token, group_id, debug=False, asyncio=True):
        self.__token = token
        self.api_version = __api_version__
        self.url = 'https://api.vk.com/method/'
        self.group_id = group_id
        self.async_use = asyncio
        self.debug = debug
        # Api Usage
        self.api = Api(token, self.url, self.api_version)

    def run(self, wait=25):
        run_bot = RunBot(self, self.__token, self.async_use)
        run_bot.run(wait)


# Main User Auth
class User:
    def __init__(self, token, user_id, debug=False):
        self.__token = token
        self.api_version = __api_version__
        self.url = 'https://api.vk.com/method/'
        self.user_id = user_id
        self.debug = debug
        # Api Usage
        self.api = Api(token, self.url, self.api_version, user=True)
