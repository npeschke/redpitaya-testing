"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import argparse

import matplotlib.pyplot as plt

import redpitaya_scpi as scpi

import api.gen as gen
import api.trig as trig
import api.acq as acq


def eval_sipm(rp_s: scpi.scpi):
    # Setup acquisition
    acq.reset_acquisition(rp_s)
    acq.set_decimation(rp_s, 64)
    trig.set_trigger_level(rp_s, 0)
    trig.set_trigger_delay(rp_s, 0)
    acq.set_channel_gain(rp_s, 1, "HV")
    acq.set_channel_gain(rp_s, 2, "HV")

    acq.start_acquisition(rp_s)

    trig.set_trigger_mode(rp_s, "CH2_PE")

    gen.pulse_slow_analog_out(rp_s, aout=0, voltage=1.8, duration=1)
    trig.wait_for_trigd(rp_s)

    data_ch1 = acq.get_channel_data(rp_s, 1)
    data_ch2 = acq.get_channel_data(rp_s, 2)

    # data = pd.DataFrame({"CH1": data_ch1, "CH2": data_ch2})
    plt.plot(data_ch1)
    plt.plot(data_ch2, "--")

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", type=str, help="The IP adress of the RedPitaya")

    arguments = parser.parse_args()

    eval_sipm(scpi.scpi(arguments.IP))

