class DatasetInstance:

    def __init__(self, names, values, target):
        self.attributes = {}
        for index, name in enumerate(names):
            self.attributes[name] = values[index]
        self.target = target

    def getAttribute(self, name):
        return self.attributes[name]

    def setAttribute(self, name, value):
        self.attributes[name] = value

    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target = target