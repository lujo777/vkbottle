import re
from time import time


class Utils:
    def __init__(self, debug):
        self.debug = debug

    def __call__(self, text):
        if self.debug is True:
            print("[\x1b[34mVK Bottle\x1b[0m] " + re.sub('#', str(time()), text) + "\x1b[0m")