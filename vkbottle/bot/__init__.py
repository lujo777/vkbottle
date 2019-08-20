from .vkbottle import RunBot

from ..portable import __api__

from ..methods import Api

from .events import Events


# Main Bot Auth
class Bot:
    def __init__(self, token: str, group_id: int, debug=False, async_use=False, **deprecated):

        # Bot Auth
        self.__token = token
        self.group_id = group_id
        self.async_use = async_use
        self.debug = debug

        # Plugins
        self.plugin_folder: str = '#'

        # Events
        self.on = Events()

        # Optional
        self.deprecated = deprecated
        self.url = 'https://api.vk.com/method/'

        # Api Usage
        self.api = Api(token, self.url, __api__)

    def run(self, wait=25):
        run_bot = RunBot(self, self.__token, self.async_use)
        run_bot.run(wait)
