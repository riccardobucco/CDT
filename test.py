from utilities import get_dataset
from decision_tree_classifiers import ID3, classify
from dataset import DatasetInstance

dataset = getDataset("pippo.csv", "d")
decision_tree = ID3(dataset)