class TreeNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

    def getKey(self):
        return self.key

    def setKey(self, key):
        self.key = key

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
    
    def addChild(self, node):
        self.children.append(node)
    
    def getChild(self, index):
        return self.children[index]

    def getChildren(self):
        return self.children

    def hasChildren(self):
        return len(self.children)