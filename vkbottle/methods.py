from .keyboard import _keyboard
from random import randint
import requests
import six


class Api(object):
    def __init__(self, token, url, api_version, method=None):
        self.messages = VkMessages(token, url, api_version)
        self.__token = token
        self.__url = url
        self.__api_version = api_version
        self._method = method

    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return Api(
            self.__token,
            self.__url,
            self.__api_version,
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)
        method = self._method.split('.')
        if len(method) == 2:
            group = method[0]
            method = method[1]

            return Method(self.__token, self.__url, self.__api_version)(group, method, kwargs)


class VkMessages:
    def __init__(self, token, url, api_version):
        self.method = Method(token, url, api_version)

    def send(self, peer_id: int, message: str, attachment=None, keyboard=None, sticker_id=None, domain=None,
             chat_id=None, user_ids=None, lat=None, long=None, reply_to=None, forward_messages=None, payload=None,
             dont_parse_links=False, disable_mentions=False):
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

    def getConversations(self, offset=0, count=20, filter_='all', extended=None, start_message_id=None,
                         fields=None):
        request = dict(
            offset=offset,
            count=count,
            filter=filter_,
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

    def getHistoryAttachments(self, peer_id, media_type=None, start_from=None, count=None, photo_sizes=None,
                              fields=None, preserve_order=None, max_forwards_level=None):
        request = dict(
            peer_id=peer_id,
            media_type=media_type,
            start_from=start_from,
            count=count,
            photo_sizes=photo_sizes,
            fields=fields,
            preserve_order=preserve_order,
            max_forwards_level=max_forwards_level
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getHistoryAttachments', request)

    def getImportantMessages(self, count=None, offset=None, start_message_id=None, preview_length=None,
                             fields=None, extended=None):
        request = dict(
            count=count,
            offset=offset,
            start_message_id=start_message_id,
            preview_length=preview_length,
            fields=fields,
            extended=extended
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getImportantMessages', request)

    def getInviteLink(self, peer_id, reset=None):
        request = dict(
            peer_id=peer_id,
            reset=reset
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getInviteLink', request)

    def getLongPollHistory(self, ts=None, pts=None, preview_length=None, onlines=None, fields=None,
                           events_limit=None, msgs_limit=None, max_msg_id=None, lp_version=None,
                           last_n=None, credentials=None):
        request = dict(
            ts=ts,
            pts=pts,
            preview_length=preview_length,
            onlines=onlines,
            fields=fields,
            events_limit=events_limit,
            msgs_limit=msgs_limit,
            max_msg_id=max_msg_id,
            lp_version=lp_version,
            last_n=last_n,
            credentials=credentials
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getLongPollHistory', request)

    def getLongPollServer(self, need_pts=None, lp_version=None):
        request = dict(
            need_pts=need_pts,
            lp_version=lp_version
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'getLongPollServer', request)

    def isMessagesFromGroupAllowed(self, group_id, user_id):
        request = dict(
            group_id=group_id,
            user_id=user_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'isMessagesFromGroupAllowed', request)

    def markAsAnsweredConversations(self, peer_id, answered=None):
        request = dict(
            peer_id=peer_id,
            answered=answered
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'markAsAnsweredConversations', request)

    def markAsImportantConversation(self, peer_id, important=None):
        request = dict(
            peer_id=peer_id,
            important=important
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'markAsImportantConversation', request)

    def markAsRead(self, message_ids, peer_id, start_message_id=None):
        request = dict(
            message_ids=message_ids,
            peer_id=peer_id,
            start_message_id=start_message_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'markAsRead', request)

    def pin(self, peer_id, message_id):
        request = dict(
            peer_id=peer_id,
            message_id=message_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'pin', request)

    def removeChatUser(self, chat_id, user_id=None, member_id=None):
        request = dict(
            chat_id=chat_id,
            user_id=user_id,
            member_id=member_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'removeChatUser', request)

    def restore(self, message_id):
        request = dict(
            message_id=message_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'restore', request)

    def search(self, q=None, peer_id=None, date=None, preview_length=None, offset=None, count=None, extended=None,
               fields=None):
        request = dict(
            q=q,
            peer_id=peer_id,
            date=date,
            preview_length=preview_length,
            offset=offset,
            count=count,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'search', request)

    def searchConversations(self, q=None, count=None, extended=None, fields=None):
        request = dict(
            q=q,
            count=count,
            extended=extended,
            fields=fields
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'searchConversations', request)

    def setActivity(self, user_id=None, type_=None, peer_id=None):
        request = dict(
            user_id=user_id,
            type=type_,
            peer_id=peer_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'setActivity', request)

    def setChatPhoto(self, file):
        request = dict(
            file=file
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'setChatPhoto', request)

    def unpin(self, peer_id):
        request = dict(
            peer_id=peer_id
        )
        request = {k: v for k, v in request.items() if v is not None}
        return self.method('messages', 'unpin', request)


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
        if 'response' in res:
            return res['response']
        raise ValueError(res)
