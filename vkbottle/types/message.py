class Geo(object):
    type: str = None
    coordinates: dict = None
    place: dict = None


class MessageObject(object):
    id: int = None
    date: int = None
    peer_id: int = None
    from_id: int = None
    text: str = None
    random_id: int = None
    ref: str = None
    ref_source: str = None
    attachments: list = None
    important: bool = None
    geo = Geo
    payload: str = None
    fwd_messages: list = None
    reply_message: dict = None


class Message(MessageObject):
    @staticmethod
    def __call__(message: str, attachment: str = None, keyboard: list = None,
                 sticker_id: int = None, chat_id: int = None, user_ids: str = None,
                 lat: float = None, long: float = None, reply_to: int = None,
                 forward_messages: str = None, disable_mentions: int = None,
                 dont_parse_links: int = None, payload: str = None):
        pass
