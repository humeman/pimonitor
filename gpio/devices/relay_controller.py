"""
pimonitor/gpio/devices/relay_board.py

Controls a 4 channel relay board.

Designed for use with:
    -> https://www.amazon.com/gp/product/B00KTEN3TM/ref=ox_sc_act_title_5?smid=A28RI4FXFS5SV8&psc=1
"""

import gpio
from ..utils import (
        exceptions
    )

import RPi.GPIO as GPIO

class RelayController:
    def __init__(
            self
        ) -> None:

        # Make sure this is supposed to exist
        if not gpio.config.devices["relay_controller"]["enabled"]:
            raise exceptions.InitError(f"RelayController is not enabled in config.yml")
        
        self.mode = "BCM"

        self.pin_ids = {
            "0": None,
            "1": None,
            "2": None,
            "3": None
        }

        # Initialize pins
        for pin_type, pin_id in gpio.config.devices["relay_controller"]["pins"]:
            if pin_type not in self.pins:
                raise exceptions.InitError(f"RelayController does not accept pin of type {pin_type}")

            self.pin_ids[pin_type] = pin_id

        for key, value in self.pin_ids.items():
            if value is None:
                raise exceptions.InitError(f"RelayController requires a pin for {key}, but it's not defined")

        # Set each pin's type
        self.pins = {
            x: GPIO.setup(y, GPIO.OUT) for x, y in self.pin_ids.items()
        }

    def set_state(
            self,
            relays: list,
            state: bool
        ) -> None:
        """
        Sets the state of the specified relays.

        Arguments:
            relays (list): Relays to activate. Should be a list of ints.
                Relay #s are: 0, 1, 2, and 3. Don't have to set all of them.
            state (bool): State to set the relays to.
                True = on, False = off
        """
        comp = []
        
        for relay in relays:
            if str(relay) not in self.pins:
                raise exceptions.InvalidPin(f"Relay {relay} does not exist")

            # Not just calling it right away since we want to validate everything
            # before we call, so we don't end up with infinitely activated
            # relays and a crashed script.
            comp.append(self.pin_ids[str(relay)])

        # Have to invert the state - False is on
        GPIO.output(comp, not state)

    def get_state(
            self,
            relay: int
        ) -> bool:
        """
        Gets the state of a relay.

        Arguments:
            relay (int): Relay to get the state of.

        Returns:
            state (bool): State of the relay.
                True = on, False = off
        """

        if str(relay) not in self.pin_ids:
            raise exceptions.InvalidPin(f"Relay {relay} does not exist")

        # Invert again
        return not GPIO.input(self.pin_ids[str(relay)])
