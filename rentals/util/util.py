import yaml
from rentals.exception import RentalException
import os, sys
import numpy as np
import dill
import pandas as pd
from rentals.constant import *

def write_yaml_file(file_path:str, data:dict=None):
    """
    Create YAML FILE
    file_path: str
    data : dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "W") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise RentalException(e, sys) from e
    
def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise RentalException(e,sys) from e
    
def save_numpy_array_data(file_path:str, array: np.array):
    """
    Save Numpy array data to file
    file_path : str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise RentalException(e, sys) from e
    
def load_numpy_array_data(file_path:str)-> np.array:
    """
    load numpy array data from file
    file_path : str_location of file to load
    return np.array data loaded
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise RentalException(e, sys) from e