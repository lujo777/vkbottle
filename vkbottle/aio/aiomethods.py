from vkbottle.keyboard import _keyboard
from random import randint
from .asyncvkbottle import Bot


class VkMessages:
    def send(self, peer_id: int, message: str, attachment=None, keyboard=None, sticker_id=None, domain=None, chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None, payload=None, dont_parse_links=False, disable_mentions=False):
        request = dict(
            message=message,
            keyboard=_keyboard(keyboard) if keyboard is not None else None,
            attachment=attachment,
            peer_id=peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker_id,
            domain=domain,
            chat_id=chat_id,
            user_ids=user_ids,
            lat=lat,
            long=long,
            reply_to=reply_to,
            forward_messages=forward_messages,
            payload=payload,
            dont_parse_links=dont_parse_links,
            disable_mentions=disable_mentions
        )
        request = {k: v for k, v in request.items() if v is not None}
        return Bot.method('messages.send', request)

    def delete(self, message_ids, spam=False, delete_for_all=False):
        request = dict(
            message_ids=message_ids,
            spam=int(spam),
            delete_for_all=int(delete_for_all)
        )
        return Bot.method('messages.delete', request)
