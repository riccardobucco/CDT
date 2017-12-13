import argparse

from utilities import getDataset, exportGraphviz
from decision_tree_classifiers import ID3, tree_classify, random_forest, random_forest_classify, getFeatureImportances, getAccuracy
from dataset import DatasetInstance, copy_dataset
from decision_tree import DecisionNode, EndNode

# Define the arguments you can use when you run the program from a console
parser = argparse.ArgumentParser(description="Run the random forest algorithm, using a given CSV dataset.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--dataset", required=True, help="Path of the CSV dataset", dest="dataset")
parser.add_argument("-l", "--label", required=True, help="The name of the label attribute", dest="label_name")
parser.add_argument("-od", "--output-directory", required=False, default=".", help="Path of the directory where the results have to be saved", dest="output_directory")
parser.add_argument("-tf", "--training-fraction", required=False, type=float, default=0.8, help="The fraction of records reserved for the training dataset (the fraction of records reserved for the test dataset will be set accordingly)", dest="training_fraction")
parser.add_argument("-nt", "--number-of-trees", required=False, type=int, default=10, help="Number of trees that have to be trained", dest="number_of_trees")
parser.add_argument("-f", "--features", required=False, type=int, default=None, help="Number of features to consider when looking for the best split", dest="max_features")
#parser.add_argument("-s", "--seed", required=False, type=int, help="Number used to initialize the internal state of the random number generator", dest="seed")
args = parser.parse_args()

train_dataset, test_dataset = getDataset(args.dataset, args.label_name, args.training_fraction)
forest = random_forest(train_dataset, args.number_of_trees, args.max_features)
for index, decision_tree in enumerate(forest):
    exportGraphviz(str(args.output_directory) + "/tree" + str(index) + ".dot", decision_tree)
predictions = random_forest_classify(forest, test_dataset)
feature_importances = getFeatureImportances(forest)
accuracy = getAccuracy(test_dataset, predictions)

output = open(str(args.output_directory) + "/output", 'w')
output.write("DATASET\n")
output.write("\t" + str(train_dataset.countInstances()) + " training examples\n")
output.write("\t" + str(test_dataset.countInstances()) + " test examples\n")
output.write("FEATURE IMPORTANCES\n")
for index, feature_importance in enumerate(feature_importances):
    output.write("\t" + str(index+1) + ") " + str(feature_importance[0]) + ": used " + str(feature_importance[1]) + " times\n")
output.write("ACCURACY\n\t" + str(accuracy))