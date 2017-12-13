from collections import Counter


class DatasetInstance:
    """
    Class that represents an instance of a dataset
    """

    # CONSTRUCTOR
    def __init__(self, attributes_names, attributes_values, target_name, target_value):
        """
        Build a new instance

        Parameters:
            - attributes_names: names of the attributes (list of Strings)
            - attributes_values: values of the attributes (list of values)
            - target_name: the name of the target (String)
            - target_value: target value (value)
        """
        self.attributes = {}
        for index, name in enumerate(attributes_names):
            self.attributes[name] = attributes_values[index]
        self.target_name = target_name
        self.target_value = target_value

    # OBJECT REPRESENTATION
    def __repr__(self):
        """
        Return a printable representation of the object (String)
        """
        instance_representation = ""
        for attribute_name in self.attributes:
            instance_representation += "{}={},".format(str(attribute_name),
                                                       str(self.attributes[attribute_name]))
        instance_representation += str(self.target_name) + "(target)=" + str(self.target_value)
        return instance_representation

    # GETTERS
    def get_attribute_value(self, attribute_name):
        """
        Return the value related to the specified attribute (value)

        Parameters:
            - attribute_name: the name of the desired attribute
        """
        return self.attributes[attribute_name]

    def get_target_name(self):
        """
        Return the name of the target (String)
        """
        return self.target_name

    def get_target_value(self):
        """
        Return the value of the target (value)
        """
        return self.target_value


class Dataset:
    """
    Class that represents a dataset
    """

    # CONSTRUCTOR
    def __init__(self, attributes_names, target_name):
        """
        Build a new empty dataset

        Parameters:
            - attributes_names: names of the attributes (list of Strings)
            - target_name: name of the target (String)
        """
        self.attributes_names = attributes_names
        self.target_name = target_name
        self.instances = []

    # OBJECT REPRESENTATION
    def __repr__(self):
        """
        Return a printable representation of the object (String)
        """
        dataset_representation = ""
        for index, instance in enumerate(self):
            dataset_representation += "(" + str(index) + ") " + instance.__repr__() + "\n"
        return dataset_representation

    # ITERATOR
    def __iter__(self):
        return iter(self.instances)

    # GETTERS
    def get_attributes_names(self):
        """
        Return the names of the attributes (list of Strings)
        """
        return self.attributes_names

    def get_target_name(self):
        """
        Return the name of the target (String)
        """
        return self.target_name

    def get_instance(self, index):
        """
        Return the instance at the specified index (DatasetInstance)

        Parameters:
            - index: the index of the desired instance (int)
        """
        return self.instances[index]

    # SETTERS
    def add_instance(self, attributes_values, target_value):
        """
        Add a new instance to the dataset

        Parameters:
            - attributes_values: values of the attributes (list of values)
            - target_value: target value (value)
        """
        self.instances.append(DatasetInstance(self.attributes_names, attributes_values,
                                              self.target_name, target_value))

    # AGGREGATORS
    def get_target_values(self):
        """
        Return a set of all the target values in the dataset (set of values)
        """
        return set(instance.get_target_value() for instance in self)

    def get_most_common_target(self):
        """
        Return the most common target value in the dataset (value)
        """
        return Counter([instance.get_target_value() for instance in self]).most_common(1)[0][0]

    def get_attribute_values(self, attribute_name):
        """
        Return a set of all the values that a specified attribute has in the dataset (set of values)

        Parameters:
            - attribute_name: the name of the attribute (String)
        """
        return set(instance.get_attribute_value(attribute_name) for instance in self)

    def count_instances(self, target=None, attribute=None):
        """
        Return the number of instances the dataset contains, subject to some constraints

        Parameters:
            - target: the value of the target, default to None (value)
            - attribute: object with name of an attribute and the related value, default to None
              ({"name": String, "value": value})
        """
        return len(self._get_instances(target=target, attribute=attribute))

    # PRIVATE METHODS
    # These methods should not be used outside the module
    def _get_instances(self, target=None, attribute=None):
        """
        Return the instances the dataset contains, subject to some constraints
        (list of DatasetInstance)

        Parameters:
            - target: the value of the target, default to None (value)
            - attribute: object with name of an attribute and the related value, default to None
              ({"name": String, "value": value})
        """
        instances = [instance for instance in self]
        if target is not None:
            instances = [instance for instance in instances
                         if instance.get_target_value() == target]
        if attribute is not None:
            instances = [instance for instance in instances
                         if instance.get_attribute_value(attribute["name"]) == attribute["value"]]
        return instances


# UTILITY FUNCTIONS
def copy_dataset(dataset, target=None, attribute=None):
    """
    Return a copy of the dataset, taking into account only the instances that satisfy certain
    constraints (Dataset)

    Parameters:
        - target: the value of the target, default to None (value)
        - attribute: object with name of an attribute and the related value, default to None
          ({"name": String, "value": value})
    """
    instances = dataset._get_instances(target=target, attribute=attribute)
    attributes_names = [attribute_name for attribute_name in dataset.get_attributes_names()]
    if attribute is not None:
        attributes_names.remove(attribute["name"])
    new_dataset = Dataset(attributes_names, dataset.get_target_name())
    for instance in instances:
        new_dataset.add_instance([instance.get_attribute_value(attribute_name)
                                  for attribute_name in attributes_names],
                                 instance.get_target_value())
    return new_dataset
