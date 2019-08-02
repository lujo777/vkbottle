import vk_api
import requests
import json
from random import randint
from .utils import Utils
from .events import Events


# The main
class Bot(Events):
    def __init__(self, token, group_id, rps_delay=0, debug=False):
        self.session = vk_api.VkApi(token=token,)
        self.session._auth_token()
        self.session.RPS_DELAY = rps_delay
        self.group_id = group_id
        self.debug = debug
        self.utils = Utils(debug)
        self.utils('Bot was authorised successfully')

    def run(self, wait=15):
        self.utils('Found {} message decorators'.format(len(self._processor_message.keys())))
        longpoll = self.session.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        ts = longpoll['ts']
        self.utils('Started listening longpoll...')
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait={wait}"
                event = requests.post(url).json()
                print(event)
                if event['updates']:
                    obj = event['updates'][0]['object']
                    print(self._events)
                    if event['updates'][0]['type'] == 'message_new':
                        self.process_message(obj['text'], obj)
                    if event['updates'][0]['type'] in self._events:
                        self.process_event(event)
            except requests.ConnectTimeout:
                self.utils.warn('Request Connect Timeout! Reloading longpoll..')
            except Exception as e:
                print(e)
            try:
                longpoll = self.session.method(
                    'groups.getLongPollServer',
                    {"group_id": self.group_id}
                    )
                ts = longpoll['ts']
            except Exception as E:
                print(str(E))

    def process_message(self, text: str, obj):
        answer = AnswerObject(obj, self.session, self.group_id)
        self.utils('\x1b[31;1m-> MESSAGE FROM {} TEXT "{}" TIME #'.format(obj['peer_id'], obj['text']))
        if text in self._processor_message:
            self._processor_message[text](answer)
            self.utils(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    self._processor_message[text].__name__, obj['peer_id']
                ))
        else:
            self.utils(
                'New message compile decorator was not found. '\
                'Compiled with decorator \x1b[35m[on-message-undefined]\x1b[0m (from: {})'.format(
                    obj['peer_id']
                ))
            self._undefined_message_func(answer)

    def process_event(self, event):
        self.utils('\x1b[31;1m-> NEW EVENT FROM {} TYPE "{}" TIME #'.format(event['updates'][0]['object']['user_id'], event['updates'][0]['type']))
        event_compile = True
        for rule in self._events[event['updates'][0]['type']]['rule']:
            event_compile = False if event['updates'][0]['object'].get(rule[0], 'undefined') != rule[1] else True
        if event_compile:
            answer = AnswerObject(event['updates'][0]['object'], self.session, self.group_id)
            self.utils('* EVENT RULES => TRUE. COMPILING EVENT')
            self._events[event['updates'][0]['type']]['call'](answer)

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response


class AnswerObject:
    def __init__(self, obj, session: vk_api.VkApi, group_id):
        self.obj = obj
        self.peer_id = obj["peer_id"] if 'peer_id' in obj else obj['user_id']
        self.session = session
        self.group_id = group_id

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response

    def __call__(self, text, attachment=None, keyboard=None, sticker=None):
        request = dict(
            message=text,
            keyboard=keyboard,
            attachment=attachment,
            peer_id=self.peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = _keyboard(self, keyboard)
        return self.method('messages', 'send', request)

    def send(self, peer_id, text, attachment=None, keyboard=None, sticker=None):
        request = dict(
            message=text,
            keyboard=keyboard,
            attachment=attachment,
            peer_id=peer_id,
            random_id=randint(1, 2e5),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = _keyboard(self, keyboard)
        return self.method('messages', 'send', request)


def _keyboard(pattern, one_time=False):
    """Simple keyboard constructor
    :param pattern: Keyboard simple pattern, check github readme
    :param one_time: Should keyboard be hidden after first use?
    :return: VK Api Keyboard JSON
    """
    rows = pattern
    buttons = list()
    for row in rows:
        row_buttons = list()
        for button in row:
            row_buttons.append(dict(
                action=dict(
                    type="text" if 'type' not in button else button['type'],
                    label=button['text'],
                    payload=json.dumps("" if 'payload' not in button else button['payload'])
                ),
                color="default" if 'color' not in button else button['color']
            )
            )
        buttons.append(row_buttons)

    keyboard = str(json.dumps(
        dict(
            one_time=one_time,
            buttons=buttons
        ),
        ensure_ascii=False
    ).encode('utf-8').decode('utf-8'))

    return keyboard