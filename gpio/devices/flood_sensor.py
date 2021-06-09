"""
pimonitor/gpio/devices/flood_sensor.py

Reads from the flood water sensor.

Designed for use with:
    -> https://www.amazon.com/gp/product/B079YB1T8J/ref=ox_sc_act_title_1?smid=APASTYW8E3D58&psc=1
"""

import gpio
from ..utils import (
        exceptions
    )

import RPi.GPIO as GPIO

class FloodSensor:
    def __init__(
            self
        ) -> None:

        # Make sure this is supposed to exist
        if not gpio.config.devices["flood_sensor"]["enabled"]:
            raise exceptions.InitError(f"FloodSensor is not enabled in config.yml")
        
        self.mode = "BCM"

        self.pin_ids = {
            "pud": None
        }

        # Initialize pins
        for pin_type, pin_id in gpio.config.devices["flood_sensor"]["pins"]:
            if pin_type not in self.pins:
                raise exceptions.InitError(f"FloodSensor does not accept pin of type {pin_type}")

        for key, value in self.pin_ids.items():
            if value is None:
                raise exceptions.InitError(f"FloodSensor requires a pin for {key}, but it's not defined")

        # Set each pin's type
        self.pins = {
            "pud": GPIO.setup(self.pin_ids["pud"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        }

    def sense(
            self
        ) -> bool:
        """
        Checks if there's water in the sensor.

        Returns:
            water (bool): True if there's water
        """
        return not GPIO.input(self.pin_ids["pud"])
