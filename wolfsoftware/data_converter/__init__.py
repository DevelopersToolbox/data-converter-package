"""
A data converter Python package.

Attributes:
- __version__: The version of the package, retrieved from the package metadata.
- __all__: A list of all public symbols that the module exports.
"""

import importlib.metadata

from .exceptions import DataConverterError
from .dataconverter import DataConverter

try:
    __version__: str = importlib.metadata.version('wolfsoftware.data_converter')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__: list[str] = [
    'DataConverter',
    'DataConverterError'
]
