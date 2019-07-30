"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi


def reset_acquisition(rp_s: scpi.scpi):
    """
    Resets oscilloscope
    :param rp_s: scpi connection object to RedPitaya
    """
    rp_s.tx_txt("ACQ:RST")