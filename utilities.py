import csv
from random import sample

from dataset import Dataset
from decision_tree import EndNode


def get_dataset(filename, target_name, training_fraction):
    """
    Return a Dataset, using the data in the CSV file (Dataset)

    Parameters:
        - filename: name of the file that contains the data (String)
        - target_name: name of the target in the csv file
        - training_fraction: The fraction of records reserved for the training dataset (number)
    """
    csv_reader = csv.DictReader(open(filename))
    attributes_names = [attribute_name for attribute_name in csv_reader.fieldnames
                        if attribute_name != target_name]
    train_dataset = Dataset(attributes_names, target_name)
    test_dataset = Dataset(attributes_names, target_name)
    instances = []
    for row in csv_reader:
        instances.append(([row[attribute_name] for attribute_name in attributes_names],
                          row[target_name]))
    all_instances_indexes = set(range(0, len(instances)))
    number_of_training_instances = int(len(all_instances_indexes) * training_fraction)
    training_instances_indexes = set(sample(all_instances_indexes, number_of_training_instances))
    test_instances_indexes = all_instances_indexes.difference(training_instances_indexes)
    for instance_index in training_instances_indexes:
        train_dataset.add_instance(instances[instance_index][0], instances[instance_index][1])
    for instance_index in test_instances_indexes:
        test_dataset.add_instance(instances[instance_index][0], instances[instance_index][1])
    return train_dataset, test_dataset

def export_graphviz(filename, decision_tree):
    """
    Print on the output file info about a tree using the DOT language

    Parameters:
        - filename: name of the file where the content must be written (String)
        - decision_tree: the tree that has to be represented using the DOT language
          (DecisionNode or EndNode)
    """
    # This function is private and should not be used outside the scope of the parent function
    def _export_node(node, output):
        if isinstance(node, EndNode):
            output.write("\t\"{}\" [label=\"{}\"]\n".format(str(id(node)),
                                                            str(node.get_target_value())))
            return
        output.write("\t\"" + str(id(node)) + "\" [label=\"\"]\n")
        for decision_attribute_value in node.children.keys():
            output.write("\t\"{}\" -> \"{}\" [label=\"{}={}\"]\n".format(str(id(node)),
                                                                         str(id(node.get_child(decision_attribute_value))),
                                                                         str(node.get_decision_attribute()),
                                                                         str(decision_attribute_value)))
            _export_node(node.get_child(decision_attribute_value), output)
    output = open(filename, 'w')
    output.write("digraph G {\n")
    _export_node(decision_tree, output)
    output.write("}")
