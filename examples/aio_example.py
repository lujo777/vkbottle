from vkbottle.aio.asyncvkbottle import Bot, AnswerObject

bot = Bot('682f0b0b7b0e396dfb2465f14c6f73252ab28ffb1cb48ff7a2ce17efce99ba36c90dc913fba8f1bad412e', 181909496, debug=False)
admin_id = 168656722  # VK Group admin ID


@bot.on_message('Hi')
async def hi(answer: AnswerObject):  # Type container is needed for syntax highlighting
    await answer('Hi my friend!')


@bot.on_message('goodbye')
async def goodbye(answer: AnswerObject):
    await answer('Ooh.. Bye-bye :)')
    await answer.send(admin_id, 'User said goodbye to bot :(')


@bot.on_message_undefined()
async def undefined(answer: AnswerObject):
    # answer('I didnt understand you :|')
    print(f"User ({answer.peer_id}) typed something undefined")

if __name__ == "__main__":
    bot.run()
