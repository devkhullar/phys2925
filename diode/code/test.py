from scipy.optimize import curve_fit
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os 
import sys

fontsize = 15

forward_bias = pd.read_csv('../data/part1_forward_bias.txt', delimiter='\t')
voltage = forward_bias['V (V)']
current = forward_bias['I (A)']
def diode_equation_test(V, I0, n):
    e = 1.60217663e-19  # Electron charge
    k = 1.380649e-23   # Boltzmann constant
    T = 300            # Temperature in Kelvin
    # Vt = (k * T) / e
    # return I0 * (np.exp(V / (n * Vt)) - 1)
    return np.log10(I0 * ((np.exp((e * V) / (n * k * T)) - 1)))

curr = np.log10(current[3:])
volt = voltage[3:]

popt, pcov = curve_fit(diode_equation_test, volt, curr)
print(*popt)
print(np.sqrt(np.diag(pcov)))

plt.errorbar(
    np.log10(volt),
    curr,
    fmt='o',
    # fill='none'
    # xerr=np.log10(current_err[3:]).abs(),
    # yerr=np.log10(voltage_err[3:]).abs()
)

plt.plot(
    np.log10(volt), 
    diode_equation_test(volt, *popt),
    c='k'
)
plt.show()