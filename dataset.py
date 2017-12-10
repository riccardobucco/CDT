class DatasetInstance:

    def __init__(self, attributes_names, attributes_values, target_value):
        self.attributes = {}
        for index, name in enumerate(attributes_names):
            self.attributes[name] = attributes_values[index]
        self.target_value = target_value

    def getAttribute(self, attribute_name):
        return self.attributes[attribute_name]

    def setAttribute(self, attribute_name, attribute_value):
        self.attributes[attribute_name] = attribute_value

    def getTarget(self):
        return self.target_value

    def setTarget(self, target_value):
        self.target_value = target_value

class Dataset:

    def __init__(self, attributes_names, target_name):
        self.attributes_names = attributes_names
        self.target_name = target_name
        self.instances = []
    
    def getTargetName(self):
        return self.target_name

    def getSetOfTargets(self):
        return set([instance.getTarget() for instance in self])

    def countInstances(self, target = None):
        if target is None:
            return len([instance for instance in self])
        return len([instance for instance in self if instance.getTarget() is target])

    def getAttributesNames(self):
        return self.attributes_names

    def addInstance(self, attributes_values, target_value):
        self.instances.append(DatasetInstance(self.attributes_names, attributes_values, target_value))

    def getInstance(self, index):
        return self.instances[index]

    def __iter__(self):
        return iter(self.instances)