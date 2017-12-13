from __future__ import division
from math import log
from random import randint, sample

from dataset import copy_dataset, Dataset
from decision_tree import DecisionNode, EndNode


# PUBLIC FUNCTIONS
def random_forest(dataset, n_of_trees, max_features):
    """
    Return a list of decision trees, built using random samples of the dataset

    Parameters:
        - dataset: the dataset used to train the classifier (Dataset)
        - n_of_trees: the number of trees that have to be trained (number)
        - max_features: the number of features to consider when looking for the best split (number)
    """
    forest = []
    for _1 in range(0, n_of_trees):
        random_dataset = Dataset(dataset.get_attributes_names(), dataset.get_target_name())
        for _2 in range(0, dataset.count_instances()):
            random_instance = dataset.get_instance(randint(0, dataset.count_instances()-1))
            attributes_values = [random_instance.get_attribute_value(attribute_name)
                                 for attribute_name in dataset.get_attributes_names()]
            target_value = random_instance.get_target_value()
            random_dataset.add_instance(attributes_values, target_value)
        forest.append(ID3(random_dataset, max_features))
    return forest

def ID3(dataset, max_features=None):
    """
    Return a decision tree classifier, computed using the ID3 algorithm (DecisionNode or EndNode)

    Parameters:
        - dataset: the dataset used to train the classifier (Dataset)
        - max_features: the number of features to consider when looking for the best split (number)
    """
    if len(dataset.get_target_values()) == 1:
        return EndNode(dataset.get_instance(0).get_target_value())
    if len(dataset.get_attributes_names()) == 0:
        return EndNode(dataset.get_most_common_target())
    best_attribute = _get_best_attribute(dataset, max_features)
    decision_node = DecisionNode(best_attribute)
    for attribute_value in dataset.get_attribute_values(best_attribute):
        if dataset.count_instances(target=None, attribute={"name": best_attribute,
                                                           "value": attribute_value}) == 0:
            child = EndNode(dataset.get_most_common_target())
            decision_node.add_child(attribute_value, child)
        else:
            child = ID3(copy_dataset(dataset, attribute={"name": best_attribute,
                                                         "value": attribute_value}), max_features)
            decision_node.add_child(attribute_value, child)
    return decision_node

def get_accuracy(dataset, predictions):
    """
    Return the accuracy of the predictions (number)

    Parameters:
        - dataset: the dataset containing all the instances correctly classified (Dataset)
        - predictions: a list of targets related to the instances of the dataset (List of values)
    """
    return sum([1 for index, instance in enumerate(dataset)
                if predictions[index] == dataset.get_instance(index).get_target_value()])/dataset.count_instances()

def tree_classify(decision_tree, instance):
    """
    Return the target value that the decision tree associates to the given instance (value)

    Parameters:
        - decision_tree: decision tree that determines which target is associated to the instance
          (DecisionNode or EndNode)
        - instance: the instance that has to be classified (DatasetInstance)
    """
    if isinstance(decision_tree, EndNode):
        return decision_tree.get_target_value()
    decision_attribute_name = decision_tree.get_decision_attribute()
    if instance.get_attribute_value(decision_attribute_name) not in decision_tree.children:
        return None
    return tree_classify(decision_tree.get_child(instance.get_attribute_value(decision_attribute_name)), instance)

def random_forest_classify(forest, dataset):
    """
    Return the target values that the random forest associates to the given dataset (List ofvalue)

    Parameters:
        - forest: random forest that determines which target is associated to the instance
          (List of DecisionNode or EndNode)
        - dataset: the dataset that has to be classified (DatasetInstance)
    """
    # This function is private and should not be used outside the scope of the parent function
    def _classify_instance(forest, instance):
        targets = {}
        for decision_tree in forest:
            target_value = tree_classify(decision_tree, instance)
            if target_value in targets:
                targets[target_value] += 1
            else:
                targets[target_value] = 1
        return max(targets, key=targets.get)
    predictions = []
    for instance in dataset:
        predictions.append(_classify_instance(forest, instance))
    return predictions

def get_feature_importances(forest):
    """
    Return an ordered list of features used in the forest, according to its importance

    Parameters:
        - forst: random forest from which the importance of the features can be estimated
    """
    features = {}
    # These functions should not be used outside the scope of the parent function
    def _get_feature_importances(decision_tree):
        if isinstance(decision_tree, EndNode):
            return
        if decision_tree.get_decision_attribute() in features:
            features[decision_tree.get_decision_attribute()] += 1
        else:
            features[decision_tree.get_decision_attribute()] = 1
        for decision_attribute_value in decision_tree.children.keys():
            _get_feature_importances(decision_tree.get_child(decision_attribute_value))
    for decision_tree in forest:
        _get_feature_importances(decision_tree)
    return [(feature, features[feature])
            for feature in sorted(features, key=features.get, reverse=True)]


# PRIVATE FUNCTIONS
# These functions should not be used outside the module
def _get_best_attribute(dataset, max_features=None):
    """
    Return the attribute of the dataset that best classifies examples of the dataset (String)

    Parameters:
        - dataset: the dataset on which the computation has to be done (Dataset)
        - max_features: the number of features to consider when looking for the best split (number)
    """
    attributes_names = dataset.get_attributes_names()
    if max_features is not None:
        attributes_names = sample(attributes_names, min(max_features, len(attributes_names)))
    max_information_gain = _information_gain(dataset, attributes_names[0])
    best_attribute = attributes_names[0]
    for index in range(1, len(attributes_names)):
        attribute_name = attributes_names[index]
        information_gain = _information_gain(dataset, attribute_name)
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
    proportions = [dataset.count_instances(target=target)/dataset.count_instances()
                   for target in dataset.get_target_values()]
    return sum(-p*log(p, 2) for p in proportions)

def _information_gain(dataset, attribute_name):
    """
    Return the measure of the difference in entropy from before to after the dataset is split on the
    given attribute (in other words, how much uncertainty in the dataset was reduced after splitting
    the dataset on the given attribute) (number)

    Parameters:
        - dataset: the dataset on which the information gain has to be computed (Dataset)
        - attribute_name: the name of the attribute with which the information gain has to be
          computed (String)
    """
    T = set()
    attribute_values = dataset.get_attribute_values(attribute_name)
    for attribute_value in attribute_values:
        t = copy_dataset(dataset, attribute={"name": attribute_name, "value": attribute_value})
        T.add(t)
    return _entropy(dataset) - sum(_entropy(t)*t.count_instances()/dataset.count_instances()
                                   for t in T)
