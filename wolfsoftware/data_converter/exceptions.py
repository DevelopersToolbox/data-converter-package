"""
This module defines custom exceptions for the importable template package.

Classes:
    - DataConverterError: A custom exception class with a default error message.
"""


class DataConverterError(Exception):
    """
    A custom exception class with a default error message.

    Attributes:
        message (str): The error message for the exception.
    """

    def __init__(self, message: str = "Data conversion error.") -> None:
        """
        Initialize the DataConverterError with an optional error message.

        Arguments:
            message (str): The error message for the exception. Defaults to "Data conversion error.".
        """
        super().__init__(message)
