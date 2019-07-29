#!/usr/bin/python
"""
Author      Nicolas Peschke
Date        26.07.2019
"""

import redpitaya_scpi as scpi
import time

rp_s = scpi.scpi("10.11.79.149")

for _ in range(100):
    rp_s.tx_txt(f"ANALOG:PIN AOUT0,1.8")
    time.sleep(1)
    rp_s.tx_txt(f"ANALOG:PIN AOUT0,0.1")
    time.sleep(1)
