from .utils import Utils
from .events import Events
from .jsontype import json_type_utils, dumps as json_dumps
from .methods import Api
from .keyboard import _keyboard
from .vkbottle import AnswerObject, RunBot


# The main
class Bot(Events):
    def __init__(self, token, group_id, debug=False, asyncio=True):
        self.__token = token
        self.api_version = 5.101
        self.url = 'https://api.vk.com/method/'
        self.group_id = group_id
        self.async_use = asyncio
        self.debug = debug
        # Api Usage
        self.api = Api(token, self.url, self.api_version)

    def run(self, wait=25):
        runbot = RunBot(self, self.__token, self.async_use)
        runbot.run(wait)
