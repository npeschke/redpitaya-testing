"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import time

import redpitaya_scpi as scpi

SLOW_AOUTS = [0, 1, 2, 3]


def reset_gen(rp_s: scpi.scpi):
    """
    Resets the signal generator
    :param rp_s: scpi connection object to RedPitaya
    """
    rp_s.tx_txt("GEN:RST")


def pulse_slow_analog_out(rp_s: scpi.scpi, aout: int, voltage: float, duration: float):
    """
    Turns specified slow analog output on for specified length, then off again.
    :param rp_s: scpi connection object to RedPitaya
    :param aout: Number of the analog output to pulse.
    :param voltage: Peak voltage
    :param duration: Peak duration in seconds
    """
    if aout not in SLOW_AOUTS:
        raise AttributeError(f"Your specified slow analog output ({aout}) is not in the list of slow analog outputs ({SLOW_AOUTS})!")
    if (voltage > 1.8) or (voltage < 0):
        raise AttributeError(f"Your specified voltage ({voltage}) is out of range (0-1.8V)!")
    if duration < 0:
        raise AttributeError(f"You cannot specify a negative duration!")

    rp_s.tx_txt(f"ANALOG:PIN AOUT{aout},{voltage}")
    time.sleep(duration)
    rp_s.tx_txt(f"ANALOG:PIN AOUT{aout},0")
