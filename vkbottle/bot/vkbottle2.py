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
MAIN BOT LONGPOLL CONSTRUCTOR
"""

from ..portable import __version__ as VERSION, API_VERSION
from ..utils import Logger, HTTP, path_loader
from ..methods import Method, Api
from .. import notifications as nf
from .events import Events, processor
from aiohttp import ClientSession, ClientConnectionError, ClientTimeout
import asyncio
from .patcher import Patcher
from multiprocessing import Pool

import time


class LongPollBot(HTTP, processor.UpdatesProcessor):
    """
    Standart LongPoll VK Bot engine

    Use LongPollBot object to manage plugins or use it in its own. Be sure
    """
    wait: int

    def __init__(self, token: str, group_id: int, plugin_folder: str = None,
                 debug: bool = False, use_regex: bool = True):
        """
        Bot Main Auth
        :param token: VK Api Token
        :param group_id:
        :param plugin_folder: Path to plugin folder. None if plugins are not in use
        :param debug: Should VKBottle show debugging messages
        """

        self.group_id: int = group_id
        self.logger: Logger = Logger(debug=debug)
        self.use_regex: bool = use_regex

        self.session = ClientSession
        self._loop = asyncio.get_event_loop

        self.on: Events = Events(use_regex=use_regex)
        self._method: Method = Method(token)
        self.api: Api = Api(self._method)

        self.patcher = Patcher(logger=self.logger)

        # [Support] Plugin Support
        # Added v0.20#master
        self._plugins = path_loader.load_plugins(plugin_folder, self.logger)

    def run(self, wait: int = 25):
        """
        Run Bot Async start coroutine
        :param wait: Long Request max waiting time (25 is recommended, max - 90)
        """
        self.wait = wait
        loop = self._loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self._loop().run_until_complete(self.logger.warn(nf.keyboard_interrupt))

    async def start(self):
        """
        LongPoll Bot runner
        todo RU -  сделать нормальную функцию проверки версии
        """

        current_portable = {'version': '0.14'}  # await self.get_current_portable()
        """
        Check newest version of VKBottle and alarm if newer version is available
        """
        if current_portable['version'] != VERSION:
            await self.logger(nf.newer_version.format(current_portable['version']))
        else:
            await self.logger(nf.newest_version)

        # [Feature] If LongPoll is not enabled in the group it automatically stops
        # Added v0.19#master
        # todo RU - сделать это нечто менее врезающимся в глаза окда
        longPollEnabled = await self.api.request('groups', 'getLongPollSettings', {'group_id': self.group_id})

        if longPollEnabled:

            # [Feature] Merge messages dictionaries
            # Added v0.20#master
            # todo RU - убрать это в отдельный враппер
            self.on.merge_processors()

            """for plugin in self._plugins:
                self.on.append_plugin(plugin)  # fixme"""

            longPollServer = await self.get_server()

            await self.logger(nf.module_longpoll.format(API_VERSION))

            # pool = Pool(processes=1)

            # pool.apply_async(self._run, [longPollServer])

            await self._run(longPollServer)
        else:

            await self.logger(nf.longpoll_not_enabled)

    async def get_server(self) -> dict:
        """
        Get an longPoll server for long request create
        :return: LongPoll Server
        """
        return await self.api.groups.getLongPollServer(group_id=self.group_id)

    async def make_long_request(self, longPollServer: dict) -> dict:
        """
        Make longPoll request to the VK Server. Comes off after wait time
        :param longPollServer:
        :return: VK LongPoll Event
        """
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
                    longPollServer['server'],
                    longPollServer['key'],
                    longPollServer['ts'],
                    self.wait
                )
        return await self.request.post(url)

    async def _run(self, longPollServer: dict):
        while True:
            try:
                event = await self.make_long_request(longPollServer)
                print(event)
                self.a = time.time()
                await self.new_update(event)
                longPollServer = await self.get_server()

            except ClientConnectionError or ClientTimeout:
                # No internet connection
                await self.logger.warn(nf.request_connection_timeout)
