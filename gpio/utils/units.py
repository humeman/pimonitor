"""
pimonitor/gpio/utils/units.py

Converts units.
"""

def to_fahrenheit(
        value: int
    ) -> int:
    """
    Converts a temperature to Fahrenheit from Celsius.

    Arguments:
        value (int): Temperature in celsius
    
    Returns:
        temperature (int): Temperature in fahrenheit
    """
    return (value * 1.8) + 32