from vkbottle import Bot

bot = Bot('my-token', 1, debug=True)
admin_id = 1  # VK Group admin ID


@bot.on_message_undefined()
def who_i_am(answer):
    answer('I can only change ur gender..')


@bot.on_message('now my gender is <gender>')
def new_gender(answer, gender):
    answer(f'Ok, now your gender is {gender}')


if __name__ == "__main__":
    bot.run()
