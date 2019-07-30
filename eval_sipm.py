"""
Author      Nicolas Peschke
Date        30.07.2019
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np

import redpitaya_scpi as scpi

import api.gen as gen
import api.trig as trig
import api.acq as acq


def eval_sipm(rp_s: scpi.scpi):
    # Setup acquisiton
    acq.reset_acquisition(rp_s)
    acq.set_decimation(rp_s, 64)
    trig.



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", type=str, help="The IP adress of the RedPitaya")

    arguments = parser.parse_args()

    eval_sipm(scpi.scpi(arguments.IP))

