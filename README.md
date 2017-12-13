# Decision trees with categorical variables support
- The ID3 algorithm creates a decision tree, finding for each node the feature that will yield the largest information gain for categorical targets. However, **scikit-learn implementation of this algorithm does not support categorical variables**.
- A random forest is an ensemble learning method for classification that operates by constructing a multitude of decision trees at training time and outputting the class that is the mode of the classes of the individual trees.

## Quick start
If you just want to quickly build and test a random forest on your CSV dataset containing categorical variables, you can run the `main.py` script. It can be used with the following parameters:
- `-d` Path of the CSV dataset
- `-l` The name of the label attribute
- `-od` Path of the directory where the results will be saved
- `-tf` The fraction of records reserved for the training dataset (the fraction of records reserved for the test dataset will be set accordingly)
- `-nt` Number of tree to be trained
- `-f` Number of features to consider when looking for the best split

For example, to predict the price in the [Car Evaluation](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation) dataset:

```python main.py --dataset=car.data --label=price```

## Docs
The `classifiers.py` file contains the main functions:
- **random_forest**(*dataset*, *n_of_trees*, *max_features*)

  Return a list of decision trees, built using random samples of the dataset.
  
  Arguments:
  - *dataset*: Dataset used to train the classifier.
  - *n_of_trees*: Number of trees that have to be trained.
  - *max_features*: Number of features to consider when looking for the best split.

- **ID3**(*dataset*, *max_features*)

  Return a list of decision trees, built using random samples of the dataset.
  
  Arguments:
  - *dataset*: Dataset used to train the classifier.
  - *max_features*: Number of features to consider when looking for the best split.

- **random_forest_classify**(*forest*, *dataset*)

  Return the target value that the random forest associates to the given instance.
  
  Arguments:
  - *forest*: Random forest that determines which target is associated to the instance
  - *dataset*: Dataset used to train the classifier.

- **id3_classify**(*forest*, *dataset*)

  Return the target value that the decision tree associates to the given instance.
  
  Arguments:
  - *decision_tree*: Decision tree that determines which target is associated to the instance
  - *dataset*: Dataset used to train the classifier.