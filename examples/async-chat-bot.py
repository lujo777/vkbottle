from vkbottle import Bot

bot = Bot('my-token', 1, debug=True, use_async=True)
admin_id = 1  # VK Group admin ID


@bot.on.message('Hi')
async def hi(answer):
    a = await answer('Hi my friend!')
    await answer('Oh sorry! You are not my friend!')
    bot.api.messages.delete(a, delete_for_all=True)


@bot.on.message_chat('<a> * <b>')
async def um(ans, a, b):
    if a.isdigit() and b.isdigit():
        await ans('it\'s {}'.format(int(a) * int(b)))
    else:
        await ans('Do you know what integers are?')


if __name__ == '__main__':
    bot.run()
