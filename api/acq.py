"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import numpy as np

import redpitaya_scpi as scpi

import api.misc as misc

DECIMATIONS = [1, 8, 64, 1024, 8192, 65535]
CHANNELS = [1, 2]
GAINS = ["HV", "LV"]


def start_acquisition(rp_s: scpi.scpi):
    """
    Starts the acquisition
    :param rp_s: scpi connection object to RedPitaya
    """
    rp_s.tx_txt("ACQ:START")


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
    # Check input_string
    misc.check_input(dec, DECIMATIONS, "decimation")

    rp_s.tx_txt(f"ACQ:DEC {dec}")


def set_channel_gain(rp_s: scpi.scpi, channel: int, gain: str):
    """
    Sets gain (HV/LV) for a channel. To be used together with the jumper settings of the channels.
    :param rp_s: scpi connection object to RedPitaya
    :param channel: Channel, either 1 or 2
    :param gain: Gain, either HV for full range +-20V or LV for +-!V
    """
    # Check input
    misc.check_input(gain, GAINS, "gain")
    misc.check_input(channel, CHANNELS, "channel")

    rp_s.tx_txt(f"ACQ:SOUR{channel}:GAIN {gain}")


def get_channel_data(rp_s: scpi.scpi, channel: int):
    """
    Retrieves data from selected channel
    :param rp_s: scpi connection object to RedPitaya
    :param channel: Channel, either 1 or 2
    :return: Numpy array containing the data
    """
    # Check input
    misc.check_input(channel, CHANNELS, "channel")

    rp_s.tx_txt(f"ACQ:SOUR{channel}:DATA?")
    buff_string = rp_s.rx_txt()

    acq_data = np.genfromtxt(buff_string.strip('{}\n\r').replace("  ", "").split(','))

    return acq_data
