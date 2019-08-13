# vkbottle
Ноовый репозиторий для быстрой и удобной работы с Vk API с использованием **декораторов**, как в известном фреймворке Flask!

[![PyPI](https://badge.fury.io/py/vkbottle.svg)](https://pypi.org/project/vkbottle/) 
[![VK Chat](https://img.shields.io/badge/Чат-Вконтакте-blue)](https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj) 
[![Build Status](https://travis-ci.com/timoniq/vkbottle.svg?branch=master)](https://travis-ci.com/timoniq/vkbottle)

## Установка

Чтобы установить, воспользуйтесь командами в терминале:  
`pip install vkbottle` или  
 `pip3 install vkbottle`  
   
 Поддерживаемые версии:  
 * Python 3.5
 * Python 3.6
 * Python 3.7 и >

## Использование

Давайте создадим простой движок бота
```python
from vkbottle import Bot, AnswerObject

bot = Bot(token, group_id, debug=True)
```
Аргумент | Значение
------------ | -------------
token | Токен вашей группы (**str**)
group_id | ID вашей группы с ботом (**int** )
debug | Нужно ли показывать дебаг-сообщения? По умолчанию False (**bool**)
asyncio | Нужно ли использовать async в смеси с мультипроцессигом для достижения более высоких результатов в скорости? По умолчанию True (**bool**)

Теперь нам нужно испортировать файл с обработкой событий (плагинов) так: `import events` с `bot.run()` в последнем из них или сделать все это в одном файле

### Использование декораторов

#### @on_message(text)
```python
@bot.on_message('hi!')
def hi(answer):
    print('Кто-то написал мне "hi!"!')
# bot.run()
```
#### @on_message_undefined()
```python
@bot.on_message_undefined()
def undefined(answer):
    print('Я кого-то не понял..')
# bot.run()
```
Как использовать **answer**?
Поддерживаются такие методы:

Метод | Описание
------------ | -------------
answer(text, attachment=None, keyboard=None, sticker=None) | Needed for fast answer to creator of event

Examples:  
```python
@bot.on_message('cat')
def itz_cat(answer: AnswerObject):
    answer('Myaaw')
# When user send message "cat" to bot, it answers "Myaaw"
```
Answer это messages.send метод без peer_id, он заполняется автоматически

### Ключи декораторов

Если это нужно, вы можете добавлять ключи в ваши декораторы так:  
```python
@bot.on_message('My name is <name>')
def my_name(answer: AnswerObject, name):
    answer('You name is ' + name + '!')
```
В декораторах сообщений из чатов это тоже поддерживается  
**Ключи возвращаются как именованные аргументы, поэтому должны быть обозначены так же как и в декораторе**

### Создание клавиатуры

Давайте сделаем простую клавиатуру, используя VKBottle Keyboard Generator:
```python
[ # My keyboard
    [{'text': 'button1'}, {'text': 'button2'}], # первая строчка
    [{'text': 'button3'}] # вторая строчка
]
```
Клавиатура:  
{button1}{button2}  
{-------button3-----}  

Опции клавиатуры:  

Опция | Значение | По умолчанию
------ | ------- | -------
text | Текст кнопки | 
color | Цвет кнопки | Default(secondary)
type | Тип действия кнопки | text

**С Answer**

```python
answer(
    'It\'s my keyboard!',
    keyboard=[
        [{'text': 'My Balance'}, {'text': 'Me'}],
        [{'text': 'shop', 'color': 'positive'}]
    ]
)
```

### Answer-Parsers

Есть два типа парсеров, всего парсеров 3:

Парсер | Описание
------ | -----------
user | method parser, основан на user.get методе
group | method parser, основан на group.getById методе
self | class parser, основан на данных значениях Bot class

Как использовать **answer-parsers**? Это очень просто:  

#### Как парсеры работают

Когда вы используете метод answer, он автоматически проверяется на парсеры.  
Парсер должен выглядеть примерно так:  
**{parser:arg}**

Например:  
```Hello, my dear {user:first_name}!```

#### User Method Parser

Парсер | Описание
-------------- | -----------
{user:first_name} | Оставляет имя владельца события
{user:last_name} | Оставляет фамилию владельца события
{user:id} | Оставляет ID владельца события

#### Group Method Parser

Парсер | Описание
-------------- | -----------
{group:name} | Оставляет имя группы бота
{group:description} | Оставляет описание группы бота
... | ...

Больше информации в [VK Object/Group Documentation](https://vk.com/dev/objects/group)

#### Self Parser

Самый быстрый парсер, нужен когда время - главный приоритет

Парсер | Описание
-------------- | -----------
{self:peer_id} | ID владельца события
{self:group_id} | ID группы бота

### Bot Api

Вы можете использовать все методы Vk API:

```python
api = bot.api
api.messages.send(peer_id=1, message='Hi, my friend!')
```

Все методы можно найти здесь [VK Methods Documentation](https://vk.com/dev/methods)
***
Подсветку имеют только эти группы методов:
* messages
***

### User Api

Чтобы авторизовать пользователя используйте:
```python
from vkbottle import User
user = User('my-token', user_id=1)
```
Аргумент | Описание
-------- | -----------
token | Vk Api токен (**str**)
user_id | Пользовательский ID (**int**)
debug | Нужно ли показывать дебаг-сообщения. По умолчанию False (**bool**)

**User Api** имеет идентичный синтаксис с Bot Api без подсветки синтаксиса запроса:
```python
# ...
user_api = user.api
user_api.messages.send(peer_id=1, message='Привет, мой коллега!', random_id=100)
```
