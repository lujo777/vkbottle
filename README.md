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

#### on_message(text)
```python
@bot.on_message('hi!')
def hi(answer):
    print('Somebody wrote me "hi!"!')
# bot.run()
```
#### on_message_undefined()
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

Answer is messages.send method without peer_id, it completes automatically

## Bot Api

You can use VK Bot API to make all types and groups of requests. To do it you can use a simple method:

```python
api = bot.api
api.messages.send(peer_id=1, message='Hi, my friend!')
```

All available methods you can find in [VK Methods Documentation](https://vk.com/dev/methods)
***
But now available methods are:
* messages.send
* messages.delete