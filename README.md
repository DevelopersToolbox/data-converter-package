<!-- markdownlint-disable -->
<p align="center">
    <a href="https://github.com/DevelopersToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/developerstoolbox/black-and-white-circle-256.png" alt="DevelopersToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/data-converter-package/actions/workflows/cicd.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/DevelopersToolbox/data-converter-package/cicd.yml?branch=master&label=build%20status&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/blob/master/LICENSE.md">
        <img src="https://img.shields.io/github/license/DevelopersToolbox/data-converter-package?color=blue&label=License&style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package">
        <img src="https://img.shields.io/github/created-at/DevelopersToolbox/data-converter-package?color=blue&label=Created&style=for-the-badge" alt="Created">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/data-converter-package/releases/latest">
        <img src="https://img.shields.io/github/v/release/DevelopersToolbox/data-converter-package?color=blue&label=Latest%20Release&style=for-the-badge" alt="Release">
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/releases/latest">
        <img src="https://img.shields.io/github/release-date/DevelopersToolbox/data-converter-package?color=blue&label=Released&style=for-the-badge" alt="Released">
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/releases/latest">
        <img src="https://img.shields.io/github/commits-since/DevelopersToolbox/data-converter-package/latest.svg?color=blue&style=for-the-badge" alt="Commits since release">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/data-converter-package/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/data-converter-package/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

The `wolfsoftware.data-converter` module provides functionalities for converting data between JSON, XML, and YAML formats.
It includes methods to convert dictionaries to and from these formats, making it a versatile tool for data transformation in Python applications.

## Installation

First, install the package using pip:

```bash
pip install wolfsoftware.data-converter
```

## Usage

### Importing the Module

To use the `DataConverter` class, import it from the `wolfsoftware.data_converter` package:

```python
from wolfsoftware.data_converter import DataConverter, DataConverterError
```

### Initializing the DataConverter

The `DataConverter` class requires data and its type as parameters during initialization. Supported data types are `json`, `xml`, `dict`, and `yaml`.

```python
# JSON data example
json_data = '{"name": "John", "age": 30}'
converter = DataConverter(json_data, data_type='json')

# XML data example
xml_data = '<person><name>John</name><age>30</age></person>'
converter = DataConverter(xml_data, data_type='xml')

# Dictionary data example
dict_data = {'name': 'John', 'age': 30}
converter = DataConverter(dict_data, data_type='dict')

# YAML data example
yaml_data = 'name: John\nage: 30\n'
converter = DataConverter(yaml_data, data_type='yaml')
```

### Converting Data

#### To JSON

Convert the data to JSON format using the `to_json` method:

```python
json_output = converter.to_json()
print(json_output)
```

#### To XML

Convert the data to XML format using the `to_xml` method:

```python
xml_output = converter.to_xml()
print(xml_output)
```

#### To YAML

Convert the data to YAML format using the `to_yaml` method:

```python
yaml_output = converter.to_yaml()
print(yaml_output)
```

### Example Usage

Here's a complete example demonstrating how to convert a dictionary to JSON, XML, and YAML formats:

```python
from wolfsoftware.data_converter import DataConverter, DataConverterError

# Dictionary data
data = {'name': 'John', 'age': 30}

# Initialize DataConverter
converter = DataConverter(data, data_type='dict')

# Convert to JSON
json_output = converter.to_json()
print("JSON Output:")
print(json_output)

# Convert to XML
xml_output = converter.to_xml()
print("XML Output:")
print(xml_output)

# Convert to YAML
yaml_output = converter.to_yaml()
print("YAML Output:")
print(yaml_output)
```

### Handling Unsupported Data Types

If an unsupported data type is provided, a `DataConverterError` will be raised:

```python
try:
    converter = DataConverter(data, data_type='unsupported')
except DataConverterError as e:
    print(f"Error: {e}")
```

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20on%20behalf%20of%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
