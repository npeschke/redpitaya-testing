"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi

DECIMATIONS = [1, 8, 64, 1024, 8192, 65535]


def reset_acquisition(rp_s: scpi.scpi):
    """
    Resets oscilloscope
    :param rp_s: scpi connection object to RedPitaya
    """
    rp_s.tx_txt("ACQ:RST")


def set_decimation(rp_s: scpi.scpi, dec: int):
    """
    Sets the decimation for the acquisition and thus the sampling rate and buffer length.
    :param rp_s: scpi connection object to RedPitaya
    :param dec: Decimation, must be in [1, 8, 64, 1024, 8192, 65535]
    """
    if dec not in DECIMATIONS:
        raise AttributeError(f"Your specified decimation ({dec}) is not in the list of poosible decimations ({DECIMATIONS})")

    rp_s.tx_txt(f"ACQ:DEC {dec}")
