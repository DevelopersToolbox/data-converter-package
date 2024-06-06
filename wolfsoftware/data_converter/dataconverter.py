"""
This module demonstrates basic functionalities including a simple greeting function and a custom exception.

Functions:
- say_hello: Returns a greeting message.
- raise_exception: Raises a custom exception ExampleCustomError.
"""
from typing import Any, Union, Dict

import json
import xml.etree.ElementTree as ET  # nosec: B405

import yaml

from defusedxml.ElementTree import fromstring
from defusedxml.minidom import parseString

from .exceptions import DataConverterError


class DataConverter:
    """
    A class for converting data between JSON, XML, and YAML formats.

    Attributes:
        data: The data to be converted.
        data_type (str): The type of data ('json', 'xml', 'dict', 'yaml').

    Methods:
        to_json: Converts data to JSON format.
        to_xml: Converts data to XML format.
        to_yaml: Converts data to YAML format.
        dict_to_xml: Converts a dictionary to XML format.
        xml_to_json: Converts XML data to JSON format.
        json_to_xml: Converts JSON data to XML format.
        yaml_to_dict: Converts YAML data to a dictionary.
    """

    def __init__(self, data: Union[str, Dict[str, Any]], data_type: str = 'json') -> None:
        """
        Initialize the DataConverter with data and data type.

        Arguments:
            data: The data to be converted.
            data_type (str): The type of data ('json', 'xml', 'dict', 'yaml'). Defaults to 'json'.

        Raises:
            DataConverterError: If data_type is unsupported.
        """
        if data_type not in {'json', 'xml', 'dict', 'yaml'}:
            raise DataConverterError("Unsupported data type")

        self.data: Union[str, Dict[str, Any]] = data
        self.data_type: str = data_type

    def to_json(self) -> str:
        """
        Convert the data to JSON format.

        Returns:
            str: The data in JSON format.

        Raises:
            DataConverterError: If the data type is unsupported for JSON conversion.
        """
        if self.data_type == 'xml':
            if isinstance(self.data, str):
                return self.xml_to_json(self.data)
            raise DataConverterError("Invalid data type for XML conversion")
        if self.data_type == 'yaml':
            if isinstance(self.data, str):
                return json.dumps(self.yaml_to_dict(self.data))
            raise DataConverterError("Invalid data type for YAML conversion")
        if self.data_type == 'dict':
            return json.dumps(self.data)
        raise DataConverterError("Unsupported data type for JSON conversion")

    def to_xml(self) -> str:
        """
        Convert the data to XML format.

        Returns:
            str: The data in XML format.

        Raises:
            DataConverterError: If the data type is unsupported for XML conversion.
        """
        if self.data_type == 'json':
            if isinstance(self.data, (str, bytes, bytearray)):
                return self.json_to_xml(json.loads(self.data))
            raise DataConverterError("Invalid data type for JSON conversion")
        if self.data_type == 'dict':
            if isinstance(self.data, dict):
                return self.dict_to_xml(self.data)
            raise DataConverterError("Invalid data type for dict conversion")
        if self.data_type == 'yaml':
            if isinstance(self.data, str):
                return self.dict_to_xml(self.yaml_to_dict(self.data))
            raise DataConverterError("Invalid data type for YAML conversion")
        raise DataConverterError("Unsupported data type for XML conversion")

    def to_yaml(self) -> str:
        """
        Convert the data to YAML format.

        Returns:
            str: The data in YAML format.

        Raises:
            DataConverterError: If the data type is unsupported for YAML conversion.
        """
        if self.data_type == 'json':
            if isinstance(self.data, (str, bytes, bytearray)):
                return yaml.dump(json.loads(self.data))
            raise DataConverterError("Invalid data type for JSON conversion")
        if self.data_type == 'dict':
            if isinstance(self.data, dict):
                return yaml.dump(self.data)
            raise DataConverterError("Invalid data type for dict conversion")
        if self.data_type == 'xml':
            if isinstance(self.data, str):
                dict_data: Dict[str, Any] = self._xml_to_dict_recursive(fromstring(self.data))
                return yaml.dump(dict_data)
            raise DataConverterError("Invalid data type for XML conversion")
        raise DataConverterError("Unsupported data type for YAML conversion")

    @staticmethod
    def dict_to_xml(data: Dict[str, Any], root_tag: str = 'root') -> str:
        """
        Convert a dictionary to XML format.

        Arguments:
            data (dict): The data to be converted.
            root_tag (str): The root tag for the XML. Defaults to 'root'.

        Returns:
            str: The data in XML format.
        """
        root = ET.Element(root_tag)
        DataConverter._dict_to_xml_recursive(data, root)
        return parseString(ET.tostring(root)).toprettyxml()

    @staticmethod
    def _dict_to_xml_recursive(data: Any, parent: ET.Element) -> None:
        """
        Recursively convert a dictionary to XML.

        Arguments:
            data: The data to be converted.
            parent: The parent XML element.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.Element(key)
                parent.append(child)
                DataConverter._dict_to_xml_recursive(value, child)
        elif isinstance(data, list):
            for item in data:
                child = ET.Element('item')
                parent.append(child)
                DataConverter._dict_to_xml_recursive(item, child)
        else:
            parent.text = str(data)

    @staticmethod
    def xml_to_json(xml_data: str) -> str:
        """
        Convert XML data to JSON format.

        Arguments:
            xml_data (str): The XML data to be converted.

        Returns:
            str: The data in JSON format.
        """
        root: ET.Element = fromstring(xml_data)
        data_dict: Dict[str, Any] = DataConverter._xml_to_dict_recursive(root)
        return json.dumps(data_dict)

    @staticmethod
    def _xml_to_dict_recursive(element: ET.Element) -> Dict[str, Any]:
        """
        Recursively convert XML data to a dictionary.

        Arguments:
            element: The XML element to be converted.

        Returns:
            dict: The data as a dictionary.
        """
        data_dict: Dict[str, Any] = {}
        # Process element attributes
        for k, v in element.attrib.items():
            data_dict['@' + k] = v
        # Process child elements
        children = list(element)
        if children:
            child_dict: Dict[str, Any] = {}
            for dc in map(DataConverter._xml_to_dict_recursive, children):
                for key, value in dc.items():
                    if key in child_dict:
                        if not isinstance(child_dict[key], list):
                            child_dict[key] = [child_dict[key]]
                        child_dict[key].append(value)
                    else:
                        child_dict[key] = value
            data_dict.update(child_dict)
        # Process element text
        text: str | None = element.text.strip() if element.text and element.text.strip() else None
        if text and not children:
            return {element.tag: text}
        if text:
            data_dict['#text'] = text
        return {element.tag: data_dict} if element.attrib or children else data_dict

    @staticmethod
    def json_to_xml(json_data: Dict[str, Any], root_tag: str = 'root') -> str:
        """
        Convert JSON data to XML format.

        Arguments:
            json_data (dict): The JSON data to be converted.
            root_tag (str): The root tag for the XML. Defaults to 'root'.

        Returns:
            str: The data in XML format.
        """
        return DataConverter.dict_to_xml(json_data, root_tag)

    @staticmethod
    def yaml_to_dict(yaml_data: str) -> Dict[str, Any]:
        """
        Convert YAML data to a dictionary.

        Arguments:
            yaml_data (str): The YAML data to be converted.

        Returns:
            dict: The data as a dictionary.
        """
        return yaml.safe_load(yaml_data)
