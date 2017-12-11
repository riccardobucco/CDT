from dataset import Dataset, DatasetInstance, copy_dataset
from decision_tree import DecisionNode, EndNode
from utilities import informationGain


def getBestAttribute(dataset):
    attributes_names = dataset.getAttributesNames()
    max_information_gain = informationGain(dataset, attributes_names[0])
    best_attribute = attributes_names[0]
    for index in range(1, len(attributes_names)):
        attribute_name = attributes_names[index]
        information_gain = informationGain(dataset, attribute_name)
        if information_gain > max_information_gain:
            max_information_gain = information_gain
            best_attribute = attribute_name
    return best_attribute

def ID3(dataset):
    # TODO: check if the dataset is empty
    if len(dataset.getTargets()) is 1:
        return DecisionTree(dataset.getTargetName(), dataset.getInstance(0).getTarget())
    if len(dataset.getAttributesNames()) is 0:
        return DecisionTree(dataset.getTargetName(), getMostCommonTarget(dataset))
    best_attribute = getBestAttribute(dataset)
    decision_tree = DecisionTree(splitting_attribute = best_attribute)
    for attribute_value in dataset.getAttributes(best_attribute):
        if dataset.countInstances(attribute = {"name": best_attribute, "value": attribute_value}) is 0:
            child = DecisionTree(target = getMostCommonTarget(dataset))
            decision_tree.addChild(attribute_value, child)
        else:
            child = ID3(copy_dataset(dataset, attribute = {"name": best_attribute, "value": attribute_value}))
            decision_tree.addChild(attribute_value, child)
    return decision_tree