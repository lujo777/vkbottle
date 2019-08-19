# Plugins

## How to use plugins?

Since v0.20#master Bot Auth option `plugin_folder` is available. `plugin_folder` is OS path to folder with plugins.
```python
# FILE /mybot.py
# You can do it like this
bot = Bot('my-token', group_id, debug=True, plugin_folder='plugins')
# Or like this
bot.plugin_folder = 'plugins'

if __name__ == '__main__':
    bot.run()
```
Default `plugin_folder` value is `'plugins'`. If plugin directory wasn't found it will be created with the `plugin_folder` path

## How to make a plugin

```python
# FILE /plugins/my_plugin.py
# You should import bot from mybot.py
from mybot import bot
from vkbottle.plugin import Plugin
# Now we should make a plugin variable
plugin = Plugin(bot, name='My super Plugin') # *
```
Plugin options:

Argument | Description | Regular/Optional
-------- | ----------- | ----------------
bot | vkbottle.Bot | Regular
name | Name of your plugin | Optional
description | Description of your plugin | Optional
priority | Priority of your plugin in events queue | Optional

Now we can use `plugin` to make message and events functions
```python
@plugin.on.message_both('plugin works?')
def wrapper(ans):
    ans('PlUgIN WOrKs!!')
```