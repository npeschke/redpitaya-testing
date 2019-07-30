"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi


def reset_gen(rp_s: scpi.scpi):
    """
    Resets the signal generator
    :param rp_s: scpi connection object to RedPitaya
    """
    rp_s.tx_txt("GEN:RST")
