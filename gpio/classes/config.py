import os
import traceback
import yaml
import inspect

import gpio # For config validation
from ..utils import (
        exceptions
    )

class Config:
    def __init__(
            self,
            path: str = "config.yml"
        ) -> None:

        self.path = path

        # Check if file exists
        if not os.path.exists(self.path):
            raise exceptions.FileError(f"File {self.path} does not exist")

        # Try to read it
        try:
            with open(self.path, "r") as f:
                self._raw = yaml.safe_load(f) 

        except:
            raise exceptions.FileError(f"File {self.path} could not be read")

        # Validate values
        self.validate()

        # Expand values
        self.expand()

    def expand(
            self
        ) -> None:

        # Make sure data is actually populated
        if not hasattr(self, "_raw"):
            raise exceptions.InitError(f"Can't expand values: _raw isn't set")

        # Set attributes
        for key, value in self._raw.items():
            setattr(self, key, value)

    def validate(
            self
        ) -> None:

        # Make sure data is populated
        if not hasattr(self, "_raw"):
            raise exceptions.InitError(f"Can't expand values: _raw isn't set")

        # Check against expected config
        try:
            with open(f"{os.path.dirname(inspect.getfile(gpio))}/expected.config.yml", "r") as f:
                self._expected = yaml.safe_load(f)

        except:
            raise exceptions.FileError("Expected config file is invalid")

        # Check every value in _raw against _expected
        for key, value in self._expected.items():
            # Check if exists
            if key not in self._raw:
                raise exceptions.ConfigError(f"Key {key} is missing from config.yml")

            # Check validity
            current_type = type(self._raw[key])
            expected_type = type(value)
            if current_type != expected_type:
                raise exceptions.ConfigError(f"Key {key} must be of type {expected_type}, not {current_type}")