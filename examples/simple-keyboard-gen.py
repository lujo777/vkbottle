from vkbottle import Bot

bot = Bot('my-token', 1, debug=True, asyncio=True)
admin_id = 1  # VK Group admin ID


@bot.on.message('dobby show keyboard')
def keyboard(answer):
    answer('Ok guurls take ur bibs!',
           keyboard=[
               [{'text': 'Call the police'}],
               [{'text': 'Yeah!'}, {'text': 'dobby skip it'}]
           ])


@bot.on.message('dobby skip it')
def keyboard_skip(answer):
    answer('Ok..',
           keyboard=[]  # This keyboard is empty!
           )


if __name__ == "__main__":
    bot.run()