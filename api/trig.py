"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import redpitaya_scpi as scpi
import api.misc as misc

MODES = ["DISABLED", "NOW", "CH1_PE", "CH1_NE", "CH2_PE", "CH2_NE", "EXT_PE", "EXT_NE", "AWG_PE", "AWG_NE"]


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


def set_trigger_mode(rp_s: scpi.scpi, mode: str):
    """
    Sets the trigger mode
    :param rp_s: scpi connection object to RedPitaya
    :param mode: Trigger mode one of [DISABLED, NOW, CH1_PE, CH1_NE, CH2_PE, CH2_NE, EXT_PE, EXT_NE, AWG_PE, AWG_NE]
    """
    # Check input_string
    misc.check_input(mode, MODES, "trigger mode")

    rp_s.tx_txt(f"ACQ:TRIG {mode}")
