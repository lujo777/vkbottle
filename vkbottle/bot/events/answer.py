from pydantic import BaseModel

from ...types import message


class AnswerObject(BaseModel, message.MessageObject):
    def __call__(self, *args, **kwargs):
        print('че ты сделол')
