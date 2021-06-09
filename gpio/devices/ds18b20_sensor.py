"""
pimonitor/gpio/devices/ds18b20_sensor.py

Reads from the DS18B20 digital temperature sensor.

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
import glob
import time

class DS18B20Sensor:
    def __init__(
            self
        ) -> None:

        # Make sure this is supposed to exist
        if not gpio.config.devices["ds18b20_sensor"]["enabled"]:
            raise exceptions.InitError(f"DS18B20Sensor is not enabled in config.yml")
        
        self.mode = "BCM"

        self.sensors = {}

        sensor_list = glob.glob("/sys/bus/w1/devices/28*")
        friendly_sensor_list = [
            sensor.rsplit("/", 1)[-1] for sensor in sensor_list
        ]

        for sensor in gpio.config.devices["ds18b20_sensor"]["addresses"]:
            if sensor not in friendly_sensor_list:
                raise exceptions.InvalidSensor(f"Sensor {sensor} was not found")

            s_id = sensor.rsplit("/", 1)[-1]

            self.sensors[s_id] = {
                "id": s_id,
                "path": f"{sensor}/w1_slave"
            }

    def _read_raw(
            self,
            sensor: str
        ):
        """
        Reads the raw value from a sensor.

        Arguments:
            sensor (str): Sensor ID

        Returns:
            value (int): Raw value
        """
        # Get sensor info
        if sensor not in self.sensors:
            raise exceptions.InvalidSensor(f"Sensor {sensor} is not registered - run self.register() to re-detect")

        sensor_info = self.sensors[sensor]

        # Get the raw value
        found = False
        cycles = 0

        while not found and cycles <= 10:
            try:
                with open(sensor_info["path"], "r") as f:
                    data = f.readlines()
                
            except:
                raise exceptions.ReadError(f"Could not read sensor file for {sensor}")

            if data[0].strip()[-3:] == "YES":
                found = True

            else:
                cycles += 1
                time.sleep(0.1) # TODO: Use non-blocking sleep. May cause problems later. Asyncio?
            
        if cycles >= 10:
            raise exceptions.ReadError(f"Sensor {sensor} timed out after 10 attempts")

        temp_location = data[1].find("t=")

        if temp_location == -1:
            raise exceptions.ReadError(f"Sensor {sensor} returned no value")

        return float(data[1][temp_location + 2:]) / 1000

    def read(
            self,
            sensor: str,
            fahrenheit: bool = False
        ) -> int:
        """
        Reads from a sensor.

        Arguments:
            sensor (str): Sensor ID
            fahrenheit (bool): If True, converts to F

        Returns:
            temperature (int): Temperature in specified units
        """

        temperature = self._read_raw(sensor)

        return units.to_fahrenheit(temperature) if fahrenheit else temperature
