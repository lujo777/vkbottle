import re
import time


class Utils:
    """Coloring class, engine of all debug messages and warns
    """
    def __init__(self, debug):
        self.debug = debug

    def __call__(self, text):
        if self.debug is True:
            print("[\x1b[34mVK Bottle\x1b[0m] " + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), text) + "\x1b[0m")

    def warn(self, text):
        if self.debug is True:
            print("[\x1b[34mVK Bottle WARN\x1b[0m] \x1b[93;1m" + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), text) + "\x1b[0m")

    @staticmethod
    def error(text):
        print("[\x1b[34mVK Bottle CRITICAL ERROR\x1b[0m] \x1b[31;1m" + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), text) + "\x1b[0m")