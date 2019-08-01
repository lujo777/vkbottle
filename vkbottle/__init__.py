import vk_api
import requests
import ujson
import random
import six

from enum import Enum


def _keyboard(pattern, one_time=False):
    rows = pattern
    buttons = list()
    for row in rows:
        row_buttons = list()
        for button in row:
            row_buttons.append(dict(
                action=dict(
                    type="text" if 'type' not in button else button['type'],
                    label=button['text'],
                    payload=ujson.dumps("" if 'payload' not in button else button['payload'])
                ),
                color="default" if 'color' not in button else button['color']
            )
            )
        buttons.append(row_buttons)

    keyboard = str(ujson.dumps(
        dict(
            one_time=one_time,
            buttons=buttons
        ),
        ensure_ascii=False
    ).encode('utf-8').decode('utf-8'))

    return keyboard


# New beta keyboard creator


class KeyboardColor(Enum):
    PRIMARY = 'primary'

    DEFAULT = 'default'

    NEGATIVE = 'negative'

    POSITIVE = 'positive'


class KeyboardButton(Enum):
    TEXT = "text"

    VKPAY = "vkpay"

    VKAPPS = "open_app"


class Keyboard(object):
    __slots__ = ('one_time', 'lines', 'keyboard')

    def __sjson_dumps(*args, **kwargs):  # this is a private function
        kwargs['ensure_ascii'] = False
        kwargs['separators'] = (',', ':')

        return ujson.dumps(*args, **kwargs)

    def __init__(self, one_time=False):
        """ Класс для создания клавиатуры для бота (https://vk.com/dev/bots_docs_3)
            :param one_time: Если True, клавиатура исчезнет после нажатия на кнопку
            :type one_time: bool
        """
        self.one_time = one_time
        self.lines = [[]]

        self.keyboard = {
            'one_time': self.one_time,
            'buttons': self.lines
        }

    def get_keyboard(self):
        """ Получить json клавиатуры """
        return self.__sjson_dumps(self.keyboard)

    @classmethod
    def get_empty_keyboard(cls):
        """ Получить json пустой клавиатуры.
        Если отправить пустую клавиатуру, текущая у пользователя исчезнет.
        """
        keyboard = cls()
        keyboard.keyboard['buttons'] = []
        return keyboard.get_keyboard()

    def add_button(self, label, color=KeyboardColor.DEFAULT, payload=None):
        """ Добавить кнопку с текстом.
                    Максимальное количество кнопок на строке - 4
                :param label: Надпись на кнопке и текст, отправляющийся при её нажатии.
                :type label: str
                :param color: цвет кнопки.
                :type color: VkKeyboardColor or str
                :param payload: Параметр для callback api
                :type payload: str or list or dict
        """

        current_line = self.lines[-1]

        if len(current_line) >= 4:
            raise ValueError('Max 4 buttons on a line')

        color_value = color

        if isinstance(color, KeyboardColor):
            color_value = color_value.value

        if payload is not None and not isinstance(payload, six.string_types):
            payload = self.__sjson_dumps(payload)

        button_type = KeyboardButton.TEXT.value

        current_line.append({
            'color': color_value,
            'action': {
                'type': button_type,
                'payload': payload,
                'label': label,
            }
        })

    def add_location_button(self, payload=None):
        """ Добавить кнопку с местоположением.
                    Всегда занимает всю ширину линии.
                :param payload: Параметр для callback api
                :type payload: str or list or dict
        """

        current_line = self.lines[-1]

        if len(current_line) != 0:
            raise ValueError(
                'This type of button takes the entire width of the line'
            )

        if payload is not None and not isinstance(payload, six.string_types):
            payload = self.__sjson_dumps(payload)

        button_type = KeyboardButton.LOCATION.value

        current_line.append({
            'action': {
                'type': button_type,
                'payload': payload
            }
        })

    def add_vkpay_button(self, vk_pay_hash, payload=None):
        """ Добавить кнопку с оплатой с помощью VKPay.
            Всегда занимает всю ширину линии.
        :param vk_pay_hash: Параметры платежа VKPay и ID приложения
        (в поле aid) разделённые &
        :type vk_pay_hash: str
        :param payload: Параметр для совместимости со старыми клиентами
        :type payload: str or list or dict
        """

        current_line = self.lines[-1]

        if len(current_line) != 0:
            raise ValueError(
                'This type of button takes the entire width of the line'
            )

        if payload is not None and not isinstance(payload, six.string_types):
            payload = self.__sjson_dumps(payload)

        button_type = KeyboardButton.VKPAY.value

        current_line.append({
            'action': {
                'type': button_type,
                'payload': payload,
                'hash': vk_pay_hash
            }
        })

    def add_vkapps_button(self, app_id, owner_id, label, vk_apps_hash, payload=None):
        """ Добавить кнопку с приложением VK Apps.
            Всегда занимает всю ширину линии.
        :param app_id: Идентификатор вызываемого приложения с типом VK Apps
        :type app_id: int
        :param owner_id: Идентификатор сообщества, в котором установлено
        приложение, если требуется открыть в контексте сообщества
        :type owner_id: int
        :param label: Название приложения, указанное на кнопке
        :type label: str
        :param vk_apps_hash: хэш для навигации в приложении, будет передан в строке
        параметров запуска после символа #
        :type vk_apps_hash: str
        :param payload: Параметр для совместимости со старыми клиентами
        :type payload: str or list or dict
        """

        current_line = self.lines[-1]

        if len(current_line) != 0:
            raise ValueError(
                'This type of button takes the entire width of the line'
            )

        if payload is not None and not isinstance(payload, six.string_types):
            payload = self.__sjson_dumps(payload)

        button_type = KeyboardButton.VKAPPS.value

        current_line.append({
            'action': {
                'type': button_type,
                'app_id': app_id,
                'owner_id': owner_id,
                'label': label,
                'payload': payload,
                'hash': vk_apps_hash
            }
        })

    def add_line(self):
        """ Создаёт новую строку, на которой можно размещать кнопки.
        Максимальное количество строк - 10.
        """

        if len(self.lines) >= 10:
            raise ValueError('Max 10 lines')

        self.lines.append([])

# End of new beta keyboard creator
# The main


class Bot:
    _processor = {}
    _undefined_func = (lambda *args: print('Add to your on-message file an on-message-undefined decorator'))

    def __init__(self, token, group_id, rps_delay=0, debug=False):
        self.session = vk_api.VkApi(token=token,)
        self.session._auth_token()
        self.session.RPS_DELAY = rps_delay
        self.group_id = group_id
        self.debug = debug

    def process_message(self, text: str, obj):
        answer = MessageAnswer(obj, self.session, self.group_id)
        if text in self._processor:
            self._processor[text](answer)
        else:
            self._undefined_func(answer)

    def on_message(self, text):
        def decorator(func):
            self._processor[text] = func
            return func
        return decorator

    def on_message_undefined(self):
        def decorator(func):
            self._undefined_func = func
            return func
        return decorator

    def run(self):
        longpoll = self.session.method(
            'groups.getLongPollServer',
            {"group_id": self.group_id}
            )
        ts = longpoll['ts']
        while True:
            try:
                url = f"{longpoll['server']}?act=a_check&key={longpoll['key']}&ts={ts}&wait=15"
                event = requests.post(url).json()
                if event['updates']:
                    if event['updates'][0]['type'] == 'message_new':
                        obj = event['updates'][0]['object']
                        self.process_message(obj['text'], obj)
            except requests.ConnectTimeout:
                print('Request Connect Timeout! Reloading longpoll..')
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

    def method(self, group, method, params):
        response = self.session.method(f"{group}.{method}", params)
        return response


class MessageAnswer:
    def __init__(self, obj, session: vk_api.VkApi, group_id):
        self.obj = obj
        self.peer_id = obj["peer_id"]
        self.attachment = obj["attachments"]
        self.fwd_message = obj["fwd_messages"]
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
            random_id=random.getrandbits(31) * random.choice([-1, 1]),
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
            random_id=random.getrandbits(31) * random.choice([-1, 1]),
            sticker_id=sticker
        )
        request = {k: v for k, v in request.items() if v is not None}
        if 'keyboard' in request:
            request['keyboard'] = _keyboard(self, keyboard)
        return self.method('messages', 'send', request)

