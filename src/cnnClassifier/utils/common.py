import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a yaml file and returns a ConfigBox object.

    Args:
        path_to_yaml (Path): Path to the yaml file.
    Raises:
        ValueError: If the yaml file is empty.
        e: If the yaml file is not found.
    Returns:
        ConfigBox: ConfigBox object containing the yaml file contents.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories.

    Args:
        path_to_directories (list): List of directory paths to be created.
        verbose (bool, optional): If True, logs the creation of directories. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves a dictionary as a json file.

    Args:
        path (Path): Path to the json file.
        data (dict): Dictionary to be saved as json.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads a json file and returns a ConfigBox object.

    Args:
        path (Path): Path to the json file.
    Raises:

        ValueError: If the json file is empty.
        e: If the json file is not found.               


    Returns:
        ConfigBox: ConfigBox object containing the json file contents.
    """
    try:
        with open(path) as f:
            content = json.load(f)
            logger.info(f"JSON file: {path} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Json file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def save_bin(path: Path, data: Any):
    """Saves data as a binary file using joblib.

    Args:
        path (Path): Path to the binary file.
        data (Any): Data to be saved as binary.
    """
    joblib.dump(data, path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads a binary file using joblib.

    Args:
        path (Path): Path to the binary file.
    Raises:
        e: If the binary file is not found.
    Returns:
        Any: Data loaded from the binary file.
    """
    try:
        data = joblib.load(path)
        logger.info(f"Binary file: {path} loaded successfully")
        return data
    except Exception as e:
        raise e
    
@ensure_annotations
def get_size(path: Path) -> str:
    """Returns the size of a file in a human-readable format.

    Args:
        path (Path): Path to the file.
    Raises:
        e: If the file is not found.
    Returns:
        str: Size of the file in a human-readable format.
    """
    try:
        size_in_bytes = os.path.getsize(path)
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        if size_in_mb >= 1:
            return f"{size_in_mb:.2f} MB"
        elif size_in_kb >= 1:
            return f"{size_in_kb:.2f} KB"
        else:
            return f"{size_in_bytes} Bytes"
    except Exception as e:
        raise e
    
def decode_image(image_base64: str) -> bytes:
    """Decodes a base64 encoded image.

    Args:
        image_base64 (str): Base64 encoded image string.
    Returns:
        bytes: Decoded image bytes.
    """
    return base64.b64decode(image_base64)

def encodeImageIntoBase64(image_path: str) -> str:
    """Encodes an image file into a base64 string.

    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Base64 encoded image string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

                        