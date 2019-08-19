# Плагины

## Как использовать плагины?

С версии v0.20#master в Bot Auth аргумент `plugin_folder` стала доступна. `plugin_folder` это путь ко всем плагинам.
```python
# FILE /mybot.py
# Можно сделать так
bot = Bot('my-token', group_id, debug=True, plugin_folder='plugins')
# Или
bot.plugin_folder = 'plugins'

if __name__ == '__main__':
    bot.run()
```
Стандартое знаяение `plugin_folder` = `'plugins'`. Если указанной директории нет - она будет создана.

## Как сделать плагин?

```python
# FILE /plugins/my_plugin.py
from mybot import bot
from vkbottle.plugin import Plugin
# Делаем обьект плагина
plugin = Plugin(bot, name='My super Plugin') # *
```
Аргументы Plugin:

Аргумент | Описание | Регулярный/Опциональный
-------- | ----------- | ----------------
bot | vkbottle.Bot | Рег.
name | Name of your plugin | Опц.
description | Description of your plugin | Опц.
priority | Priority of your plugin in events queue | Oпц.

Теперь мы можем использовать `plugin` чтобы отслеживать события
```python
@plugin.on.message_both('plugin works?')
def wrapper(ans):
    ans('PlUgIN WOrKs!!')
```
