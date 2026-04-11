from scipy.optimize import curve_fit
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os 
import sys

fontsize = 15

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def linear_fit(x, m, b):
    return m * x + b

def find_intersection(m1, b1, m2, b2):
    xi = (b2 - b1) / (m1 - m2)
    yi = m1 * xi + b1
    return xi, yi

def uncertainty(m1, b1, m1_err, b1_err, m2, b2, m2_err, b2_err):
    term1 = (b2 - b1) / (m2 - m1) * m2_err
    term2 = (b2 - b1) / (m2 - m1) * m1_err
    term3 = 1 / (m2 - m1) * b2_err 
    term4 = 1 / (m2 - m1) * b1_err
    return np.sqrt(term1**2 + term2**2 + term3**2 + term4**2)


lambda950 = pd.read_csv('../data/950nm.txt', delimiter='\t')
voltage = lambda950['V (V)']
current = lambda950['I (A)']

kink_index = 6
plt.errorbar(
    voltage, 
    current,
    fmt='o',
    xerr=lambda950['dV (V)'],
    yerr=lambda950['dI (A)'],
    label='Observed Data'
)
popt, pcov = curve_fit(linear_fit, voltage[:kink_index], current[:kink_index])
m1, b1 = popt
m1_err, b1_err = np.sqrt(np.diag(pcov))
print(f'm1 =  {m1} +- {m1_err}')
print(f'b1 = {b1} +- {b1_err}')

popt_, pcov_ = curve_fit(linear_fit, voltage[kink_index + 4:], current[kink_index + 4:])
m2, b2 = popt_
m2_err, b2_err = np.sqrt(np.diag(pcov_))
print(f'm2 =  {m2} +- {m2_err}')
print(f'b2 = {b2} +- {b2_err}')
                         
plt.plot(
    voltage[:kink_index + 8],
    linear_fit(voltage[:kink_index + 8], *popt),
    c='k',
    label='Before Kink Fit',
    zorder=10,
)
plt.plot(
    voltage[kink_index + 2:],
    linear_fit(voltage[kink_index + 2:], *popt_),
    c='red',
    zorder=12,
    label='After Kink Fit'
)

x_int, y_int = find_intersection(*popt, *popt_)
x_int_err = uncertainty(*popt, *np.sqrt(np.diag(pcov)), *popt_, *np.sqrt(np.diag(pcov_)))
print(f'x_intersection = {x_int} +- {x_int_err}')
# print(f'y_intersection')

plt.scatter(x_int, y_int, color='green', marker='x', label='Intersection')

plt.xlabel('Voltage [V]', fontsize=fontsize)
plt.ylabel('Current [A]', fontsize=fontsize)
plt.legend()
plt.show()