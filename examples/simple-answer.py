from vkbottle import Bot, AnswerObject

bot = Bot('my-token', 1, debug=True, async=True)
admin_id = 1  # VK Group admin ID


@bot.on_message('Hi')
def hi(answer: AnswerObject):  # Type container is needed for syntax highlighting
    answer('Hi my friend!')


@bot.on_message('goodbye')
def goodbye(answer: AnswerObject):
    answer('Ooh.. Bye-bye :)')
    answer.send(admin_id, 'User said goodbye to bot :(')


@bot.on_message_undefined()
def undefined(answer: AnswerObject):
    answer('I didnt understand you :|')


if __name__ == "__main__":
    bot.run()