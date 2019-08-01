from vkbottle import Bot, MessageAnswer

bot = Bot('my-token', 1, debug=True)
admin_id = 1  # VK Group admin ID


@bot.on_message('Hi')
def hi(answer: MessageAnswer):  # Type container is needed for syntax highlighting
    answer('Hi my friend!')


@bot.on_message('goodbye')
def goodbye(answer: MessageAnswer):
    answer('Ooh.. Bye-bye :)')
    answer.send(admin_id, 'User said goodbye to bot :(')


@bot.on_message_undefined()
def undefined(answer: MessageAnswer):
    answer('I didnt understand you :|')


if __name__ == "__main__":
    bot.run()