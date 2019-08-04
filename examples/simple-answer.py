from vkbottle import Bot, AnswerObject

bot = Bot('my-token', 1, debug=True, async=True)
admin_id = 1  # VK Group admin ID


@bot.on_message('Hi')
def hi(answer: AnswerObject):  # Type container is needed for syntax highlighting
    a = answer('Hi my friend!')
    answer('Oh sorry! You are not my friend!')
    bot.api.messages.delete(a, delete_for_all=True)


@bot.on_message('goodbye')
def goodbye(answer: AnswerObject):
    answer('Ooh.. Bye-bye :)')
    bot.api.messages.send(admin_id, 'User said goodbye to bot :(')


@bot.on_message_undefined()
def undefined(answer: AnswerObject):
    answer('I didnt understand you :|')


if __name__ == "__main__":
    bot.run()