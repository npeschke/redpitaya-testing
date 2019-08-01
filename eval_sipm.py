"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import argparse
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import redpitaya_scpi as scpi

import api.gen as gen
import api.trig as trig
import api.acq as acq


def eval_sipm(rp_s: scpi.scpi, num: int):
    # data = pd.DataFrame(columns=["voltage", "channel", "sample", "run"],
    #                     dtype={"voltage": "float64", "channel": "int", "sample": "int", "run": "int"})

    data = pd.DataFrame()
    for i in range(num):
        run_data = pulse_sipm(rp_s)
        run_data["run"] = i
        data = data.append(run_data)

        # data = data.append(pd.DataFrame({"CH1": data_ch1, "CH2": data_ch2, "run": i, "sample": range(16384)}))
        # data = data.append(data_ch1)
        # data = data.append(data_ch2)


        # plt.plot(data_ch1, "y", alpha=1/num)
        # plt.plot(data_ch2, "g--", alpha=1/num)

    # plt.vlines(8192, 0, 2)

    traces_fig, traces_ax = plt.subplots(figsize=(10, 5))
    #
    # traces_ax = sns.scatterplot(x="index", y="CH1", data=data, legend="run", ax=traces_ax)
    # traces_ax = sns.lineplot(x="sample", y="CH1", ci=None, data=data, hue="run", ax=traces_ax)
    # traces_ax = sns.lineplot(x="sample", y="CH2", ci=None, data=data, hue="run", ax=traces_ax)
    traces_ax = sns.lineplot(x="sample", y="voltage", ci=None, data=data, style="channel", hue="run", ax=traces_ax)
    #
    # # traces_ax.set_xlim(7000, 8200)
    #
    traces_fig.show()

    # plt.xlim(8140, 8180)
    # plt.xlim(5000, 6000)
    # plt.show()


def pulse_sipm(rp_s: scpi.scpi):
    # Setup acquisition
    acq.reset_acquisition(rp_s)
    acq.set_decimation(rp_s, 1)
    trig.set_trigger_level(rp_s, 500)
    trig.set_trigger_delay(rp_s, 17000)
    acq.set_channel_gain(rp_s, 1, "HV")
    acq.set_channel_gain(rp_s, 2, "HV")
    acq.start_acquisition(rp_s)
    trig.set_trigger_mode(rp_s, "NOW")
    gen.pulse_slow_analog_out(rp_s, aout=0, voltage=1.8, duration=0)
    trig.wait_for_trigd(rp_s)
    data_ch1 = acq.get_channel_data(rp_s, 1)
    data_ch2 = acq.get_channel_data(rp_s, 2)

    return data_ch1.append(data_ch2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", type=str, help="The IP adress of the RedPitaya")

    arguments = parser.parse_args()

    sns.set_style("darkgrid")

    rp_connection = scpi.scpi(arguments.IP)
    try:
        eval_sipm(rp_s=rp_connection, num=2)
    finally:
        rp_connection.close()
