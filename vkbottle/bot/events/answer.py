class AnswerObject(object):
    def __init__(self, obj: dict):
        self.obj = obj

    def __getattr__(self, attr):
        print(attr)

