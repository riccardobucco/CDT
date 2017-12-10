class DecisionTree:

    # COSTRUCTOR
    def __init__(self, splitting_attribute = None, target = None):
        self.splitting_attribute = splitting_attribute
        self.target = target
        self.children = {}

    # GETTERS
    def getSplittingAttribute(self):
        return self.splitting_attribute

    def getTarget(self):
        return self.target

    def getChild(self, attribute_value):
        return self.children[attribute_value]

    # SETTERS
    def addChild(self, attribute_value, node):
        self.children[attribute_value] = node