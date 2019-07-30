"""
Author      Nicolas Peschke
Date        29.07.2019
"""

import redpitaya_scpi as scpi
import time
import argparse
import numpy as np

import matplotlib.pyplot as plt


def eval_scpi_slow_out_trigger_speed(rp_ip: str):
    # Establish connection
    rp_s = scpi.scpi(rp_ip)

    # Reset acquisition
    rp_s.tx_txt(f"ACQ:RST")

    # Setup acquisition
    rp_s.tx_txt(f"ACQ:DEC 64")
    rp_s.tx_txt(f"ACQ:TRIG:LEV 0")
    rp_s.tx_txt(f"ACQ:TRIG:DLY 0")

    # Start acquisition
    rp_s.tx_txt(f"ACQ:START")
    time.sleep(1)
    rp_s.tx_txt(f"ACQ:SOUR1:GAIN HV")
    rp_s.tx_txt(f"ACQ:SOUR2:GAIN HV")
    rp_s.tx_txt(f"ACQ:TRIG AWG_PE")
    rp_s.tx_txt(f"SOUR2:TRIG:IMM")

    rp_s.tx_txt(f"ANALOG:PIN AOUT0,1.8")
    time.sleep(0.001)
    rp_s.tx_txt(f"ANALOG:PIN AOUT0,0.1")

    gen_data = get_data_on_trigger(rp_s, 2)

    data_line_plt, data_line_ax = plt.subplots()
    data_line_ax = data_line_ax.plot(gen_data)

    data_line_plt.show()


def get_data_on_trigger(rp_s, channel: int):
    wait_for_trigd(rp_s)
    rp_s.tx_txt(f"ACQ:SOUR{channel}:DATA?")
    buff_string = rp_s.rx_txt()
    gen_data = np.genfromtxt(buff_string.strip('{}\n\r').replace("  ", "").split(','))
    return gen_data


def wait_for_trigd(rp_s):
    """
    Waits until RedPitaya reports trig'd
    :param rp_s: scpi connection to RedPitaya
    """
    while True:
        rp_s.tx_txt(f"ACQ:TRIG:STAT?")
        if rp_s.rx_txt() == "TD":
            break


def eval_scpi_fast_out_trigger_speed(rp_ip: str):
    # Establish connection
    rp_s = scpi.scpi(rp_ip)

    # Reset signal generator & oscilloscope
    rp_s.tx_txt(f"GEN:RST")
    rp_s.tx_txt(f"ACQ:RST")

    # Setup siggen
    # rp_s.tx_txt(f"SOUR1:FUNC SINE")
    # rp_s.tx_txt(f"SOUR1:FREQ:FIX 1000")
    # rp_s.tx_txt(f"SOUR1:VOLT 1")

    # Setup arbitrary waveform
    # wav = [0 for _ in range(1)] + [1 for _ in range(10000)]
    wav = [0] + [1 for _ in range(10000)]

    rp_s.tx_txt(f"SOUR1:TRAC:DATA:DATA {str(wav).strip('[]').replace(' ', '')}")
    rp_s.tx_txt(f"SOUR1:FUNC ARBITRARY")

    # Set burst mode, 1 pulse
    rp_s.tx_txt(f"SOUR1:BURS:STAT ON")
    rp_s.tx_txt(f"SOUR1:BURS:NCYC 1")
    rp_s.tx_txt(f"OUTPUT1:STATE ON")

    # Setup acquisition
    rp_s.tx_txt(f"ACQ:DEC 64")
    rp_s.tx_txt(f"ACQ:TRIG:LEV 0")
    rp_s.tx_txt(f"ACQ:TRIG:DLY 0")

    # Start acquisition
    rp_s.tx_txt(f"ACQ:START")
    time.sleep(1)
    rp_s.tx_txt(f"ACQ:SOUR1:GAIN HV")
    rp_s.tx_txt(f"ACQ:SOUR2:GAIN HV")
    rp_s.tx_txt(f"ACQ:TRIG AWG_PE")
    rp_s.tx_txt(f"SOUR1:TRIG:IMM")

    while True:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    buff_string = rp_s.rx_txt()
    gen_data = np.genfromtxt(buff_string.strip('{}\n\r').replace("  ", "").split(','))

    data_line_plt, data_line_ax = plt.subplots()
    data_line_ax = data_line_ax.plot(gen_data)

    data_line_plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", type=str, help="The IP adress of the RedPitaya")

    arguments = parser.parse_args()

    # eval_scpi_fast_out_trigger_speed(rp_ip=arguments.IP)
    eval_scpi_slow_out_trigger_speed(rp_ip=arguments.IP)
