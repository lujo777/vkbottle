# vkbottle
New VK bot-engine repo with **decorators** like in famous framework flask!

[![PyPI](https://badge.fury.io/py/vkbottle.svg)](https://pypi.org/project/vkbottle/) 
[![VK Chat](https://img.shields.io/badge/Vk-Chat-blue)](https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj) 
[![Build Status](https://travis-ci.com/timoniq/vkbottle.svg?branch=master)](https://travis-ci.com/timoniq/vkbottle)

## Install

To install use terminal command:  
`pip install vkbottle` or  
 `pip3 install vkbottle`  
   
 Supported Python versions:  
 * Python 3.5
 * Python 3.6
 * Python 3.7 and >

## Usage
Lets create a simple bot engine
```python
from vkbottle import Bot, MessageAnswer

bot = Bot(token, group_id, debug=True)
```
Name | Value
------------ | -------------
token | Your VK Group token for longpoll starting (**str**)
group_id | Your VK Group ID (**int** )
debug | Should vkbottle show debug messages? Default to False (**bool**)
asyncio | Should vkbottle (Bot) use asyncio to reach more faster results. Default to True (**bool**)

Now we should import our event-files like this: `import events` with `bot.run()` in it or make it in one single file

### Usage Decorators

#### @on_message(text)
```python
@bot.on_message('hi!')
def hi(answer):
    print('Somebody wrote me "hi!"!')
# bot.run()
```
#### @on_message_undefined()
```python
@bot.message_undefined()
def undefined(answer):
    print('I cannot understand somebody')
# bot.run()
```
How to use **answer**?
There're a lot of supported methods:

Method | Description
------------ | -------------
answer(text, attachment=None, keyboard=None, sticker=None) | Needed for fast answer to creator of event

Examples:  
```python
@bot.on_message('cat')
def itz_cat(answer: AnswerObject):
    answer('Myaaw')
# When user send message "cat" to bot, it answers "Myaaw"
```
Answer is messages.send method without peer_id, it completes automatically

### Keys

If you need it, you can add simple keys to your decorators like this:  
```python
@bot.on_message('My name is <name>')
def my_name(answer: AnswerObject, name):
    answer('You name is ' + name + '!')
```
It is supported in chat-decorators too  
**Keys are named arguments to the function so should be resolved equal as it was resolved in decorator**

### Keyboard Generator

Let's make a simple keyboard using VKBottle Keyboard Generator:
```python
[ # My keyboard
    [{'text': 'button1'}, {'text': 'button2'}], # row
    [{'text': 'button3'}] # second row
]
```
Keyboard:  
{button1}{button2}  
{-------button3-----}  

Keyboard options for a button:  

Option | Meaning | Default
------ | ------- | -------
text | Button text | 
color | Button color | Default(secondary)
type | Button action type | text

**With Answer**

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

There are two types of parsers and 3 parsers at all:

Parser | Description
------ | -----------
user | method parser, based on user.get request
group | method parser, based on group.getById request
self | class parser, based on self variables of a Bot class

How to use **answer-parsers**? It's easy to explain:  

#### How parsers work

You make an answer request and the message takes part in Answer-Parser сheckup.  
Parser example looks like this:  
**{parser:arg}**

For example:  
```Hello, my dear {user:first_name}!```

#### User Method Parser

Parser Example | Description
-------------- | -----------
{user:first_name} | Make it to name of the user who made an event
{user:last_name} | Make it to second name of the user who made an event
{user:id} | Make it to id of the userwho made an event

#### Group Method Parser

Parser Example | Description
-------------- | -----------
{group:name} | Make it to name of the group where bot is
{group:description} | Make it to description of the group where bot is
... | ...

More info in [VK Object/Group Documentation](https://vk.com/dev/objects/group)

#### Self Parser

This parser is very fast, recommended to use, when time is the main priority

Parser Example | Description
-------------- | -----------
{self:peer_id} | Event Owner ID
{self:group_id} | Group where bot is ID

### Bot Api

You can use VK Bot API to make all types and groups of requests. To do it you can use a simple method:

```python
api = bot.api
api.messages.send(peer_id=1, message='Hi, my friend!')
```

All available methods you can find in [VK Methods Documentation](https://vk.com/dev/methods)
***
All groups of methods are supported but only these have special highlighting functions:
* messages
***

### User Api

To authorise user use this method:
```python
from vkbottle import User
user = User('my-token', user_id=1)
```
Argument | Description
-------- | -----------
token | Vk Api token (**str**)
user_id | User ID (**int**)
debug | Should VKBottle escape debugging messages. Default to False (**bool**)

**User Api** is equal to the Bot Api but doesn't have highlighting feature:
```python
# ...
user_api = user.api
user_api.messages.send(peer_id=1, message='Hello my colleague!', random_id=100)
```
