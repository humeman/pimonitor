"""
pimonitor/gpio/devices/dht11_sensor.py

Reads from the DHT11 humidity & temperature sensor.

Designed for use with:
    NA
"""

import gpio
from ..utils import (
        exceptions,
        units
    )

from typing import Iterable
import RPi.GPIO as GPIO
import dht11

class DHT11Sensor:
    def __init__(
            self
        ) -> None:

        # Make sure this is supposed to exist
        if not gpio.config.devices["dht11_sensor"]["enabled"]:
            raise exceptions.InitError(f"DHT11Sensor is not enabled in config.yml")
        
        self.mode = "BCM"

        self.pin_ids = {
            "read": None
        }

        # Initialize pins
        for pin_type, pin_id in gpio.config.devices["dht11_sensor"]["pins"]:
            if pin_type not in self.pins:
                raise exceptions.InitError(f"DHT11Sensor does not accept pin of type {pin_type}")

        for key, value in self.pin_ids.items():
            if value is None:
                raise exceptions.InitError(f"DHT11Sensor requires a pin for {key}, but it's not defined")

        # Create DHT11 instance
        self.dht11 = dht11.DHT11(pin = self.pin_ids["read"])

    def read(
            self,
            fahrenheit: bool = False
        ) -> Iterable[int]:
        """
        Reads from the sensor.

        Arguments:
            fahrenheit (bool): If True, converts to F

        Returns:
            temperature (int): Temperature in specified units
            humidity (int): Humidity as a value from 1-100
        """

        data = self.read()

        if not data.is_valid():
            raise exceptions.ReadError(f"Result isn't valid")

        return (units.to_fahrenheit(data.temperature) if fahrenheit else data.temperature), data.humidity
