# vkbottle
New VK bot-engine repo with decorators!

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
rps_delay | Set the server-response delay. Default to 0 (**int**)

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

