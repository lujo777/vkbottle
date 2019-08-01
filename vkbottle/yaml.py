import yaml


class Yaml:
    def __init__(self, path):
        self.path = path
        with open(path, 'r', encoding='utf-8') as config:
            self.yamlFile = config.read()
        self.data = yaml.safe_load(self.yamlFile)

    def load(self):
        return self.data

    def reload(self):
        with open(self.path, 'r', encoding='utf-8') as config:
            self.yamlFile = config.read()
        self.data = yaml.safe_load(self.yamlFile)
        return self.data
