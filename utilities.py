import csv

from dataset import Dataset, DatasetInstance


def get_dataset(filename, target_name):
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