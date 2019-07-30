"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi


def set_trigger_level(rp_s: scpi.scpi, level: float):
    """
    Set trigger level in mV
    :param rp_s: scpi connection object to RedPitaya
    :param level: Trigger level in mV
    """
    rp_s.tx_txt(f"ACQ:TRIG:LEV {level}")


def set_trigger_delay(rp_s: scpi.scpi, delay: float):
    """
    Set trigger delay in ns
    :param rp_s: scpi connection object to RedPitaya
    :param delay: Trigger delay in ns
    """
    rp_s.tx_txt(f"ACQ:TRIG:DLY {delay}")


def wait_for_trigd(rp_s: scpi.scpi):
    """
    Waits until RedPitaya reports trig'd
    :param rp_s: scpi connection object to RedPitaya
    """
    while True:
        rp_s.tx_txt(f"ACQ:TRIG:STAT?")
        if rp_s.rx_txt() == "TD":
            break
