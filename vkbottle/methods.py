from .keyboard import _keyboard
from random import randint
import requests


class Api(object):
    def __init__(self, token, url, api_version):
        self.messages = VkMessages(token, url, api_version)


class VkMessages:
    def __init__(self, token, url, api_version):
        self.method = Method(token, url, api_version)

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
        return self.method('messages', 'send', request)

    def delete(self, message_ids, spam=False, delete_for_all=False):
        request = dict(
            message_ids=message_ids,
            spam=int(spam),
            delete_for_all=int(delete_for_all)
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'delete', request)

    def deleteChatPhoto(self, chat_id):
        request = dict(
            chat_id=chat_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'deleteChatPhoto', request)

    def deleteConversation(self, user_id=None, peer_id=None):
        request = dict(
            user_id=user_id,
            peer_id=peer_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'deleteConversation', request)

    def edit(self, peer_id: int, message: str, message_id: int, attachment=None, sticker_id=None, domain=None,
             chat_id=None, user_ids=None, lat=None, long=None, keep_forward_messages=None, keep_snippets=None,
             dont_parse_links=False, disable_mentions=False):
        request = dict(
            message=message,
            message_id=message_id,
            attachment=attachment,
            peer_id=peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker_id,
            domain=domain,
            chat_id=chat_id,
            user_ids=user_ids,
            lat=lat,
            long=long,
            keep_forward_messages=keep_forward_messages,
            keep_snippets=keep_snippets,
            dont_parse_links=dont_parse_links,
            disable_mentions=disable_mentions
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'edit', request)

    def editChat(self, chat_id, title):
        request = dict(
            chat_id=chat_id,
            title=title
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'editChat', request)

    def getByConversationMessageId(self, peer_id: int, conversation_message_ids, extended=None, fields=None):
        request = dict(
            peer_id=peer_id,
            conversation_message_ids=conversation_message_ids,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getByConversationMessageId', request)

    def getById(self, message_ids, preview_length=None, extended=None, fields=None):
        request = dict(
            message_ids=message_ids,
            preview_length=preview_length,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getById', request)

    def getConversationMembers(self, peer_id: int, fields=None):
        request = dict(
            peer_id=peer_id,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getConversationMembers', request)

    def getConversations(self, offset=0, count=20, filter='all', extended=None, start_message_id=None,
                         fields=None):
        request = dict(
            offset=offset,
            count=count,
            filter=filter,
            extended=extended,
            start_message_id=start_message_id,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getConversations', request)

    def getConversationsById(self, peer_ids, extended=None, fields=None):
        request = dict(
            peer_ids=peer_ids,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getConversationsById', request)

    def getHistory(self, offset=None, count=None, user_id=None, peer_id=None, start_message_id=None,
                   rev=None, extended=None, fields=None):
        request = dict(
            offset=offset,
            count=count,
            user_id=user_id,
            peer_id=peer_id,
            start_message_id=start_message_id,
            rev=rev,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getHistory', request)

    def getHistoryAttachments(self):
        pass

    def getImportantMessages(self):
        pass

    def getInviteLink(self):
        pass

    def getLongPollHistory(self):
        pass

    def getLongPollServer(self):
        pass

    def isMessagesFromGroupAllowed(self):
        pass

    def markAsAnsweredConversations(self):
        pass

    def markAsImportantConversation(self):
        pass

    def markAsRead(self):
        pass

    def pin(self):
        pass

    def removeChatUser(self):
        pass

    def restore(self):
        pass

    def search(self):
        pass

    def searchConversations(self):
        pass

    def setActivity(self):
        pass

    def unpin(self):
        pass


class Method:
    def __init__(self, token, url, api_version):
        self.token = token
        self.url = url
        self.api_version = api_version

    def __call__(self, group, method, args):
        res = requests.post(
            f'{self.url}{group}.{method}/?access_token={self.token}&v={self.api_version}',
            data=args
        ).json()
        return res['response']
