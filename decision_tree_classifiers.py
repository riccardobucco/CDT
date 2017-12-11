from __future__ import division
from math import log

from dataset import copy_dataset
from decision_tree import DecisionNode, EndNode
from utilities import informationGain


# PUBLIC FUNCTIONS
def ID3(dataset):
    """
    Return a decision tree classifier, computed using the ID3 algorithm (DecisionNode or EndNode)
    
    Parameters:
        - dataset: the dataset used to train the classifier
    """
    if len(dataset.getTargetValues()) is 1:
        return DecisionTree(dataset.getTargetName(), dataset.getInstance(0).getTargetValue())
    if len(dataset.getAttributesNames()) is 0:
        return DecisionTree(dataset.getTargetName(), dataset.getMostCommonTarget())
    best_attribute = _getBestAttribute(dataset)
    decision_node = DecisionNode(best_attribute)
    for attribute_value in dataset.getAttributeValues(best_attribute):
        if dataset.countInstances(attribute = {"name": best_attribute, "value": attribute_value}) is 0:
            child = EndNode(dataset.getMostCommonTarget())
            decision_node.addChild(attribute_value, child)
        else:
            child = ID3(copy_dataset(dataset, attribute = {"name": best_attribute, "value": attribute_value}))
            decision_node.addChild(attribute_value, child)
    return decision_node

def classify(decision_tree, instance):
    """
    Return the target value that the decision tree associates to the given instance (value)
    
    Parameters:
        - decision_tree: decision tree that determines which target is associated to the instance (DecisionNode or EndNode)
        - instance: the instance that has to be classified (DatasetInstance)
    """
    if type(decision_tree) is EndNode:
        return decision_tree.getTargetValue()
    decision_attribute = decision_tree.getDecisionAttribute()
    return classify(decision_tree.getChild(decision_attribute), instance)
        

# PRIVATE FUNCTIONS
# These functions should not be used outside the module
def _getBestAttribute(dataset):
    """
    Return the attribute of the dataset that best classifies examples of the dataset (String)
    
    Parameters:
        - dataset: the dataset on which the computation has to be done (Dataset)
    """
    attributes_names = dataset.getAttributesNames()
    max_information_gain = _informationGain(dataset, attributes_names[0])
    best_attribute = attributes_names[0]
    for index in range(1, len(attributes_names)):
        attribute_name = attributes_names[index]
        information_gain = _informationGain(dataset, attribute_name)
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            best_attribute = attribute_name
    return best_attribute

def _entropy(dataset):
    """
    Return the entropy that characterizes the given dataset (number)
    
    Parameters:
        - dataset: the dataset on which the entropy has to be computed (Dataset)
    """
    proportions = [dataset.countInstances(target = target)/dataset.countInstances() for target in dataset.getTargetValues()]
    return sum(-p*log(p, 2) for p in proportions)

def _informationGain(dataset, attribute_name):
    """
    Return the measure of the difference in entropy from before to after the dataset is split on the
    given attribute (in other words, how much uncertainty in the dataset was reduced after splitting
    the dataset on the given attribute) (number)
    
    Parameters:
        - dataset: the dataset on which the information gain has to be computed (Dataset)
        - attribute_name: the name of the attribute with which the information gain has to be computed (String)
    """
    T = set()
    attribute_values = dataset.getAttributesNames(attribute_name)
    for attribute_value in attribute_values:
        t = copy_dataset(dataset, attribute = {"name": attribute_name, "value": attribute_value})
        T.add(t)
    return _entropy(dataset) - sum(_entropy(t)*t.countInstances()/dataset.countInstances() for t in T)