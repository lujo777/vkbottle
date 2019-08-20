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
FILE WITH LOGGERS AND LOG-FEATURES
"""

import re
import time


class Logger:
    """Coloring class, engine of all debug messages and warns
    """
    def __init__(self, debug):
        self.debug = debug

    def __call__(self, *text, separator=' '):
        if self.debug is True:
            new = ''
            for i, el in enumerate(text):
                new += str(el)
                if i + 1 != len(text):
                    new += separator
            print("[\x1b[34mVK Bottle\x1b[0m] " + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + "\x1b[0m")

    def warn(self, *text, separator=' '):
        if self.debug is True:
            new = ''
            for i, el in enumerate(text):
                new += str(el)
                if i + 1 != len(text):
                    new += separator
            print("[\x1b[34mVK Bottle WARN\x1b[0m] \x1b[93;1m" + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + "\x1b[0m")

    @staticmethod
    def error(*text, separator=' '):
        new = ''
        for i, el in enumerate(text):
            new += str(el)
            if i + 1 != len(text):
                new += separator
        print("[\x1b[34mVK Bottle CRITICAL ERROR\x1b[0m] \x1b[31;1m" + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + "\x1b[0m")

    def progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        if self.debug is True:
            prefix = "[\x1b[34mVK Bottle\x1b[0m] " + prefix
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)

            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
            # Print New Line on Complete
            if iteration == total:
                print()