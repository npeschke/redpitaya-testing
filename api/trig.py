"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi


def wait_for_trigd(rp_s: scpi.scpi):
    """
    Waits until RedPitaya reports trig'd
    :param rp_s: scpi connection to RedPitaya
    """
    while True:
        rp_s.tx_txt(f"ACQ:TRIG:STAT?")
        if rp_s.rx_txt() == "TD":
            break
