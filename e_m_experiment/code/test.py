import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit
fontsize = 15


positive = pd.read_csv('e_m_experiment/data/positive_anode_connection.csv')

for df in [positive]:
    df['I (A)'] = df['I (mA)'] / 1000
    df['dI (A)'] = df['dI (mA)'] / 1000
    # display(df)
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.errorbar(
    positive['V (V)'][1:],
    positive['I (A)'][1:],
    xerr=positive['dV (V)'][1:],
    yerr=positive['dI (A)'][1:],
    # capsize=15,
    fmt='o',
    color='blue',
    label='Data',
    # ms=15,
)
ax.set_xlabel(r'V$_a$ [V]', fontsize=fontsize)
ax.set_ylabel(r'I$_a$ [A]', fontsize=fontsize)

def power_law(x, c, k):
    return c * (x**k)

params, covariance = curve_fit(power_law, positive['V (V)'][1:], positive['I (A)'][1:])
c_fit, k_fit = params
ax.plot(
    positive['V (V)'][1:],
    power_law(positive['V (V)'][1:], c_fit, k_fit),
    c='k',
    label='Mode'
)
plt.legend()
# ax.set_yscale('log')
plt.show()