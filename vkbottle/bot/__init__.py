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
BOT MAIN API WRAPPER
"""

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
