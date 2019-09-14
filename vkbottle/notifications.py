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


from .project_collections import colored


plugin_folder = 'Plugin Folder was created, PATH "{}"'

newer_version = 'Newer version of VKBottle available ({})! ' \
                'Install it using ' + colored('pip install vkbottle --upgrade', 'yellow')

newest_version = 'You are using the newest version of VKBottle'

bot_auth = 'Bot <' + colored('{}', 'magenta') + '> was authorised successfully'

module_longpoll = 'MODULE USING LONGPOLL VERSION {}'

deprecated_name = 'Name \'{}\' is now deprecated. Use name \'{}\' and read the docs'

messages_decorators = 'Found {} message decorators'

longpoll_connection_error = 'LongPoll Connection error! Check your internet connection and try again!'

longpoll_not_enabled = 'LongPoll is not enabled in your group'

request_connection_timeout = 'Request Connect Timeout! Reloading..'

runtime_error = 'ATTENTION! Warn ({}) is called often because you use async ' \
                'functions when \'async_use\' is False or upside down!'

add_undefined = colored('Add to your on-message file an on-message-undefined decorator', 'yellow')

keyboard_interrupt = colored('VKBottle successfully stopped by Keyboard Interrupt', 'yellow')
