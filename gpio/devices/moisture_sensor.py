"""
pimonitor/gpio/devices/moisture_sensor.py

Reads from the flood water sensor.

Designed for use with:
    -> https://www.amazon.com/gp/product/B076DDWDJK/ref=ox_sc_act_title_6?smid=A243HB0NZWY05K&psc=1 
"""

import gpio
from ..utils import (
        exceptions
    )

import RPi.GPIO as GPIO

class MoistureSensor:
    def __init__(
            self
        ) -> None:

        # Make sure this is supposed to exist
        if not gpio.config.devices["moisture_sensor"]["enabled"]:
            raise exceptions.InitError(f"MoistureSensor is not enabled in config.yml")
        
        self.mode = "BCM"

        self.pin_ids = {
            "pud": None
        }

        # Initialize pins
        for pin_type, pin_id in gpio.config.devices["moisture_sensor"]["pins"]:
            if pin_type not in self.pins:
                raise exceptions.InitError(f"MoistureSensor does not accept pin of type {pin_type}")

        for key, value in self.pin_ids.items():
            if value is None:
                raise exceptions.InitError(f"MoistureSensor requires a pin for {key}, but it's not defined")

        # Set each pin's type
        self.pins = {
            "pud": GPIO.setup(self.pin_ids["pud"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        }

    def sense(
            self
        ) -> bool:
        """
        Checks if the soil moisture has crossed the threshold.
        (so, True when the soil is wet enough)

        Returns:
            water (bool): True if the threshold has been crossed
        """
        return not GPIO.input(self.pin_ids["pud"])