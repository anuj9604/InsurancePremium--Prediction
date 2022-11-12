import yaml
from premium.exception import PremiumException
from premium.logger import logging
import numpy as np
import pandas as pd
import dill
import os, sys

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the content as a dictionary
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise PremiumException(e,sys) from e

def save_numpy_array_data(file_path: str, array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise PremiumException(e,sys) from e

def save_object(file_path:str, obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            logging.info(f"Pickle object saved, file path {file_path}")
    except Exception as e:
        raise PremiumException(e,sys) from e

