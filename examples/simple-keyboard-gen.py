from vkbottle import Bot, AnswerObject

bot = Bot('my-token', 1, debug=True, asyncio=True)
admin_id = 1  # VK Group admin ID


@bot.on_message('dobby show keyboard')
def keyboard(answer: AnswerObject):
    answer('Ok guurls take ur bibs!',
           keyboard=[
               [{'text': 'Call the police'}],
               [{'text': 'Yeah!'}, {'text': 'dobby skip it'}]
           ])


@bot.on_message('dobby skip it')
def keyboard_skip(answer: AnswerObject):
    answer('Ok..',
           keyboard=[]  # This keyboard is empty!
           )


if __name__ == "__main__":
    bot.run()