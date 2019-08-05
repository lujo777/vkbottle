from .utils import Utils
from .events import Events
from .jsontype import json_type_utils, dumps as json_dumps
from .methods import Api
from .keyboard import _keyboard
from .vkbottle import RunBot, AnswerObject, RunBotAsync


# The main
class Bot(Events):
    def __init__(self, token, group_id, debug=False, asyncio=True):
        self.__token = token
        self.api_version = 5.101
        self.url = 'https://api.vk.com/method/'
        self.group_id = group_id
        self.async_use = asyncio
        self.debug = debug
        self.__utils = Utils(debug)
        self.__utils('Bot was authorised successfully')
        # Api Usage
        self.api = Api(token, self.url, self.api_version)

    def run(self, wait=25):
        if self.async_use is False:
            runbot = RunBot(self, self.__token)
            runbot.run(wait)
        else:
            runbot = RunBotAsync(self, self.__token)
            runbot.run(wait)
