from .utils import Utils
from .events import Events
from .jsontype import json_type_utils, dumps as json_dumps
from .methods import Api
from .keyboard import _keyboard
from .vkbottle import RunBot, AnswerObject, RunBotAsync
import asyncio

# The main
class Bot(Events):
    def __init__(self, token, group_id, rps_delay=0, debug=False, asyncio=True):
        self.__token = token
        self.api_version = 5.101
        self.url = 'https://api.vk.com/method/'
        self.group_id = group_id
        self.async = asyncio
        self.debug = debug
        self.__utils = Utils(debug)
        self.__utils('Bot was authorised successfully')
        # Api Usage
        self.api = Api(token, self.url, self.api_version)

    def run(self, wait=15):
        if self.async is False:
            runbot = RunBot(self, self.__token)
            runbot.run(wait)
        else:
            runbot = RunBotAsync(self, self.__token)
            runbot.run(wait)


AnswerObject = AnswerObject