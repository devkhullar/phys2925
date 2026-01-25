import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy
import math

data5 = pd.read_csv(r'C:\Users\devkh\Desktop\Phys 2925\e_m_experiment\data\5cm_part_a.csv')
data4 = pd.read_csv(r'C:\Users\devkh\Desktop\Phys 2925\e_m_experiment\data\5cm_part_a.csv')
data3 = pd.read_csv(r'C:\Users\devkh\Desktop\Phys 2925\e_m_experiment\data\5cm_part_a.csv')

def magnetic_field(df, radius, N=2):
    mu_0 = 4 * np.pi * 10**(-7)
    k = (8 * mu_0 * N) / (math.sqrt(125) * radius)
    df['B'] = k * df['I_H (A)']
    df['B^2'] = df['B']**2
    df['r^2'] = df['r (cm)']**2
    df['r^2 B^2'] = df['r^2'] * df['B^2']
    return df

data_list = [data5, data4, data3]
radius_list = [5, 4, 3]
fontsize = 15

for i in range(len(data_list)):
    data = magnetic_field(data_list[i], radius_list[i])
    x = 2 * data['V_a (V)'].to_numpy()
    y = data['r^2 B^2'].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    model = slope * x + intercept 

    fig, ax = plt.subplots(figsize=(5, 5))
    # sns.scatterplot(
    #     x=2*data['V_a (V)'], 
    #     y=data['r^2 B^2'],
    #     ax=ax,
    #     c='k'
    # )
    ax.scatter(x, y, c='k')
    ax.plot(x, model, c='b')
    ax.set_xlabel(r'$2V_a$ [V]', fontsize=fontsize)
    ax.set_ylabel(r'$r^2 B^2$ [m$^2$ T]', fontsize=fontsize)
    plt.show()