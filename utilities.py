import csv

from dataset import Dataset, DatasetInstance
from decision_tree import EndNode, DecisionNode


def getDataset(filename, target_name):
    """
    Return a Dataset, using the data in the CSV file (Dataset)
    
    Parameters:
        - filename: name of the file that contains the data (String)
        - target_name: name of the target in the csv file
    """
    csv_reader = csv.DictReader(open(filename))
    attributes_names = [attribute_name for attribute_name in csv_reader.fieldnames if attribute_name != target_name]
    dataset = Dataset(attributes_names, target_name)
    for row in csv_reader:
        dataset.addInstance([row[attribute_name] for attribute_name in attributes_names], row[target_name])
    return dataset

def exportGraphviz(filename, decision_tree):
    """
    Print on the output file info about a tree using the DOT language

    Parameters:
        - filename: name of the file where the content must be written
        - decision_tree: the tree that has to be represented using the DOT language
    """
    # This function is private and should not be used outside the scope of the parent function
    def _exportNode(node, output):
        if type(node) is EndNode:
            output.write("\t\"" + str(id(node)) + "\" [label=\"" + str(node.getTargetValue() + "\"]\n"))
            return
        output.write("\t\"" + str(id(node)) + "\" [label=\"\"]\n")
        for decision_attribute_value in node.children.keys():
            output.write("\t\"" + str(id(node)) + "\" -> \"" + str(id(node.getChild(decision_attribute_value))) + "\" [label=\"" + str(node.getDecisionAttribute()) + "=" + str(decision_attribute_value) + "\"]\n")
            _exportNode(node.getChild(decision_attribute_value), output)
    output = open(filename, 'w')
    output.write("digraph G {\n")
    _exportNode(decision_tree, output)
    output.write("}")