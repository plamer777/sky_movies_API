"""This file contains an utility function to load data from json file"""
import json
from typing import Union
# ------------------------------------------------------------------------


def read_json(filename: str, encoding: str = "utf-8") -> Union[list, dict]:
    """This function loads data from json file

    :param filename: the name of the json file
    :param encoding: the encoding of the json file

    :returns: deserialized json object like a list or dictionary
    """

    with open(filename, encoding=encoding) as f:
        return json.load(f)
