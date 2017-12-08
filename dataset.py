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

class Dataset:

    def __init__(self, names, target):
        self.names = names
        self.target = target
        self.instances = []

    def addInstance(self, values, target):
        self.instances.append(DatasetInstance(self.names, values, target))

    def getInstance(self, index):
        return self.instances[index]

    def __iter__(self):
        return iter(self.instances)