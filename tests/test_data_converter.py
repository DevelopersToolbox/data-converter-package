"""
This test module provides unit tests for the Data Converter Python Package module using pytest.

It includes tests for versioning and various data conversion functionalities.
"""

from typing import Any, Dict, Optional

import json
import importlib.metadata
from xml.etree.ElementTree import Element  # nosec: B405

import pytest
import yaml

from defusedxml.ElementTree import fromstring

from wolfsoftware.data_converter import DataConverter, DataConverterError


def test_version() -> None:
    """
    Test to ensure the version of the Package is set and not 'unknown'.

    This test retrieves the version of the package using importlib.metadata and asserts that the version
    is not None and not 'unknown'.
    """
    version: Optional[str] = None

    try:
        version = importlib.metadata.version('wolfsoftware.data_converter')
    except importlib.metadata.PackageNotFoundError:
        version = None

    assert version is not None, "Version should be set"  # nosec: B101
    assert version != 'unknown', f"Expected version, but got {version}"  # nosec: B101


def test_to_json_from_dict() -> None:
    """
    Test converting a dictionary to JSON format.
    """
    data: Dict[str, Any] = {'name': 'John', 'age': 30}
    converter = DataConverter(data, data_type='dict')
    json_data: str = converter.to_json()

    assert json.loads(json_data) == data  # nosec: B101


def test_to_json_from_xml() -> None:
    """
    Test converting XML data to JSON format.
    """
    xml_data = '<person><name>John</name><age>30</age></person>'
    converter = DataConverter(xml_data, data_type='xml')
    json_data: str = converter.to_json()
    expected_data: Dict[str, Dict[str, str]] = {'person': {'name': 'John', 'age': '30'}}

    assert json.loads(json_data) == expected_data  # nosec: B101


def test_to_json_from_yaml() -> None:
    """
    Test converting YAML data to JSON format.
    """
    yaml_data = 'name: John\nage: 30\n'
    converter = DataConverter(yaml_data, data_type='yaml')
    json_data: str = converter.to_json()
    expected_data: Dict[str, Any] = {'name': 'John', 'age': 30}

    assert json.loads(json_data) == expected_data  # nosec: B101


def test_to_xml_from_dict() -> None:
    """
    Test converting a dictionary to XML format.
    """
    data: Dict[str, Dict[str, Any]] = {'person': {'name': 'John', 'age': 30}}
    converter = DataConverter(data, data_type='dict')
    xml_data: str = converter.to_xml()
    root: Element = fromstring(xml_data)

    assert root.tag == 'root'  # nosec: B101
    name_element: Element | None = root.find('person/name')
    age_element: Element | None = root.find('person/age')
    assert name_element is not None and name_element.text == 'John'  # nosec: B101
    assert age_element is not None and age_element.text == '30'  # nosec: B101


def test_to_xml_from_json() -> None:
    """
    Test converting JSON data to XML format.
    """
    json_data = '{"person": {"name": "John", "age": 30}}'
    converter = DataConverter(json_data, data_type='json')
    xml_data: str = converter.to_xml()
    root: Element = fromstring(xml_data)

    assert root.tag == 'root'  # nosec: B101
    name_element: Element | None = root.find('person/name')
    age_element: Element | None = root.find('person/age')
    assert name_element is not None and name_element.text == 'John'  # nosec: B101
    assert age_element is not None and age_element.text == '30'  # nosec: B101


def test_to_xml_from_yaml() -> None:
    """
    Test converting YAML data to XML format.
    """
    yaml_data = 'name: John\nage: 30\n'
    converter = DataConverter(yaml_data, data_type='yaml')
    xml_data: str = converter.to_xml()
    root: Element = fromstring(xml_data)

    assert root.tag == 'root'  # nosec: B101
    name_element: Element | None = root.find('name')
    age_element: Element | None = root.find('age')
    assert name_element is not None and name_element.text == 'John'  # nosec: B101
    assert age_element is not None and age_element.text == '30'  # nosec: B101


def test_to_yaml_from_dict() -> None:
    """
    Test converting a dictionary to YAML format.
    """
    data: Dict[str, Any] = {'name': 'John', 'age': 30}
    converter = DataConverter(data, data_type='dict')
    yaml_data: str = converter.to_yaml()

    assert yaml.safe_load(yaml_data) == data  # nosec: B101


def test_to_yaml_from_json() -> None:
    """
    Test converting JSON data to YAML format.
    """
    json_data = '{"name": "John", "age": 30}'
    converter = DataConverter(json_data, data_type='json')
    yaml_data: str = converter.to_yaml()
    expected_data: Dict[str, Any] = {'name': 'John', 'age': 30}

    assert yaml.safe_load(yaml_data) == expected_data  # nosec: B101


def test_to_yaml_from_xml() -> None:
    """
    Test converting XML data to YAML format.
    """
    xml_data = '<person><name>John</name><age>30</age></person>'
    converter = DataConverter(xml_data, data_type='xml')
    yaml_data: str = converter.to_yaml()
    expected_data: Dict[str, Dict[str, str]] = {'person': {'name': 'John', 'age': '30'}}

    assert yaml.safe_load(yaml_data) == expected_data  # nosec: B101


def test_unsupported_data_type_to_json() -> None:
    """
    Test that converting an unsupported data type to JSON raises an error.
    """
    data = 'some data'
    with pytest.raises(DataConverterError):
        DataConverter(data, data_type='unsupported')


def test_unsupported_data_type_to_xml() -> None:
    """
    Test that converting an unsupported data type to XML raises an error.
    """
    data = 'some data'
    with pytest.raises(DataConverterError):
        DataConverter(data, data_type='unsupported')


def test_unsupported_data_type_to_yaml() -> None:
    """
    Test that converting an unsupported data type to YAML raises an error.
    """
    data = 'some data'
    with pytest.raises(DataConverterError):
        DataConverter(data, data_type='unsupported')


def test_dict_to_xml() -> None:
    """
    Test the conversion of a dictionary to XML using the public method.
    """
    data: Dict[str, Dict[str, Any]] = {'person': {'name': 'John', 'age': 30}}
    converter = DataConverter(data, data_type='dict')
    xml_data: str = converter.to_xml()
    root: Element = fromstring(xml_data)

    name_element: Element | None = root.find('person/name')
    age_element: Element | None = root.find('person/age')
    assert name_element is not None and name_element.text == 'John'  # nosec: B101
    assert age_element is not None and age_element.text == '30'  # nosec: B101


def test_xml_to_json() -> None:
    """
    Test converting XML data to JSON format.
    """
    xml_data = '<person><name>John</name><age>30</age></person>'
    json_data: str = DataConverter.xml_to_json(xml_data)
    expected_data: Dict[str, Dict[str, str]] = {'person': {'name': 'John', 'age': '30'}}

    assert json.loads(json_data) == expected_data  # nosec: B101


def test_xml_to_dict() -> None:
    """
    Test the conversion of XML data to a dictionary using the public method.
    """
    xml_data = '<person><name>John</name><age>30</age></person>'
    converter = DataConverter(xml_data, data_type='xml')
    json_data: str = converter.to_json()
    expected_data: Dict[str, Dict[str, str]] = {'person': {'name': 'John', 'age': '30'}}
    assert json.loads(json_data) == expected_data  # nosec: B101


def test_json_to_xml() -> None:
    """
    Test converting JSON data to XML format.
    """
    json_data: Dict[str, Dict[str, Any]] = {"person": {"name": "John", "age": 30}}
    xml_data: str = DataConverter.json_to_xml(json_data)
    root: Element = fromstring(xml_data)

    assert root.tag == 'root'  # nosec: B101
    name_element: Element | None = root.find('person/name')
    age_element: Element | None = root.find('person/age')
    assert name_element is not None and name_element.text == 'John'  # nosec: B101
    assert age_element is not None and age_element.text == '30'  # nosec: B101
