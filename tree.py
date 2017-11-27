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

class Tree:

    def __init__(self, root_node):
        self.root = root_node
    
    def __iter__(self):
        queue = []
        all_nodes = []
        queue.append(self.root)
        while len(queue) is not 0:
            current_node = queue.pop(0)
            all_nodes.append(current_node)
            queue.extend(current_node.getChildren())
        return iter(all_nodes)

    def getRoot(self):
        return self.root

    def setRoot(self, root_node):
        self.root = root_node