# vkbottle
New VK bot-engine repo with decorators!
##Usage
Lets create a simple bot engine
```python
from vkbottle import Bot, MessageAnswer

bot = Bot(token, group_id)
```
Name | Value
------------ | -------------
token | Your VK Group token for longpoll starting (str)
group_id | Your VK Group ID (int)

Now we should import our event-files like these: `import events` with `bot.run()` in it or make it in one single file

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

