from ..portable import __api__

from ..methods import Api


# Main User Auth
class User:
    def __init__(self, token, user_id, debug=False):

        # User Auth
        self.__token = token
        self.user_id = user_id

        # Optional
        self.url = 'https://api.vk.com/method/'
        self.debug = debug

        # Api Usage
        self.api = Api(token, self.url, __api__, user=True)
