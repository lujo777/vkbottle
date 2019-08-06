# vkbottle
New VK bot-engine repo with **decorators** like in famous framework flask!

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
async | Should vkbottle (Bot) use asyncio to reach more faster results. Default to True (**bool**)

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