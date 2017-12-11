class DecisionNode:
    """
    Class that represents a decision node of a decision tree
    """
    
    # CONSTRUCTOR
    def __init__(self, decision_attribute_name):
        """
        Build a new DecisionNode
        
        Parameters:
            - decision_attribute_name: the name of the attribute on which the decision have to be taken (String)
        """
        self.decision_attribute_name = decision_attribute_name
        self.children = {}

    # GETTERS
    def getDecisionAttribute(self):
        """
        Return the attribute that determines which path you should be taken (String)
        """
        return self.decision_attribute
    
    def getChild(self, decision_attribute_value):
        """
        Return the child node associated to the decision attribute value (DecisionNode or EndNode)
        
        Parameters:
            - decision_attribute_value: the decision attribute value to which the child node is associated
        """
        return self.children[decision_attribute_value]

    # SETTERS
    def addChild(self, decision_attribute_value, node):
        """
        Associate a new child to a given attribute value
        
        Parameters:
            - decision_attribute_value: the attribute value to which the child node has to be associated (value)
            - node: the child node (DecisionNode or EndNode)
        """
        self.children[decision_attribute_value] = node


class EndNode:
    """Class that represents an end node (leaf) of a decision tree"""
    
    # CONSTRUCTOR
    def __init__(self, target_value):
        """
        Build a new EndNode
        
        Parameters:
            - target_value: the target associated to the end node (value)
        """
        self.target_value = target_value
    
    def getTargetValue(self):
        """
        Return the target associated to the end node (value)
        """
        return self.target_value