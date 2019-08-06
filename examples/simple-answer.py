from vkbottle import Bot, AnswerObject

bot = Bot('35c3149d2eb58d902cde288564e58309d73bb736dff1913a70b1f0172769b0cbaf414c9cb6a65e6f6f461', 181909496, debug=True, asyncio=True)
admin_id = 168656722  # VK Group admin ID


@bot.on_message('Hi')
def hi(answer: AnswerObject):  # Type container is needed for syntax highlighting
    a = answer('Hi my friend!')
    answer('Oh sorry! {user:first_name} You are not my friend!')
    bot.api.messages.delete(a, delete_for_all=True)


@bot.on_message('goodbye')
def goodbye(answer: AnswerObject):
    answer('Ooh.. Bye-bye :)')
    bot.api.messages.send(admin_id, 'User said goodbye to bot :(')


@bot.on_group_join(join_type='accepted')
def on_join(answer: AnswerObject):
    answer('Woof! Thanks for this!')


if __name__ == "__main__":
    bot.run()
