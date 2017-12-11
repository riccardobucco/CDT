from __future__ import division
from math import log

def entropy(dataset):
    """
    Return the entropy that characterizes the given dataset (number)
    
    Parameters:
        - dataset: the dataset on which the entropy has to be computed (Dataset)
    """
    proportions = [dataset.countInstances(target = target)/dataset.countInstances() for target in dataset.getTargetValues()]
    return sum(-p*log(p, 2) for p in proportions)

def informationGain(dataset, attribute_name):
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
    return entropy(dataset) - sum(entropy(t)*t.countInstances()/dataset.countInstances() for t in T)