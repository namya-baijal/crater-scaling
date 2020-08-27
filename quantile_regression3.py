import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import linregress

data = pd.read_csv("/Users/namya/Documents/Lunar_Data/peakring_diameter.csv")
data.head()

df = pd.DataFrame(data)
df.dropna(inplace=True)
df['log_Diam'] = np.log10(df['Diameter'])
df['log_hpr'] = np.log10(df['Peak ring'])
print(df)
# print(df.var())    #function to calculate variance of diameter and depth
model = smf.quantreg('log_hpr ~ log_Diam', df)  # quantile regression plot
res = model.fit(q=.5)
print(res.summary())  # prints summary of the median quantile
quantiles = [0.1, 0.9, 0.5]
fits = [model.fit(q=q) for q in quantiles]
figure, axes = plt.subplots()
x = df['log_Diam']
y = df['log_hpr']
_x = np.linspace(x.min(), x.max(), num=len(y))  # range of x
# fits lines for the 5th and 95th percentile
_y_01 = fits[0].params['log_Diam'] * _x + fits[0].params['Intercept']
_y_09 = fits[1].params['log_Diam'] * _x + fits[1].params['Intercept']
_y_05 = fits[2].params['log_Diam'] * _x + fits[2].params['Intercept']
# start and end coordinates of fit lines
p = np.column_stack((x, y))
a = np.array([_x[0], _y_01[0]])  # first point of 0.1 quantile fit line
b = np.array([_x[-1], _y_01[-1]])  # last point of 0.1 quantile fit line

slope, intercept, r_value, p_value, std_err = linregress([_x[0], _x[-1]], [_y_01[0], _y_01[-1]])        #calculates the slope and intercept for 0.1 quantile
print('0.1 quantile:',
      'slope:', "{:.4f}".format(slope), 'intercept:', "{:.4f}".format(intercept))

a_ = np.array([_x[0], _y_09[0]])  # first point of 0.9 quantile fit line
b_ = np.array([_x[-1], _y_09[-1]])  # last point of 0.9 quantile fit line

slope, intercept, r_value, p_value, std_err = linregress([_x[0], _x[-1]], [_y_09[0], _y_09[-1]])      #calculates the slope and intercept for the 0.9 quantile
print('0.9 quantile:',
      'slope:', "{:.4f}".format(slope), 'intercept:', "{:.4f}".format(intercept))

a__ = np.array([_x[0], _y_05[0]])  # first point of median line
b__ = np.array([_x[-1], _y_05[-1]])  # last point of median line

slope, intercept, r_value, p_value, std_err = linregress([_x[0], _x[-1]], [_y_05[0], _y_05[-1]])      #calculates the slope and intercept for the 0.9 quantile
print('median:',
      'slope:', "{:.4f}".format(slope), 'intercept:', "{:.4f}".format(intercept))
axes.scatter(x, df['log_hpr'], c='k', alpha=0.6, label='data points', )
axes.plot(_x, _y_09, label=quantiles[1], c='orange')
axes.plot(_x, _y_01, label=quantiles[0], c='g')
axes.plot(_x, _y_05, label=quantiles[2], c='y')
axes.legend()

axes.set_xlabel('log(Rim-crest Diameter) [km]')
axes.set_ylabel('log(Peak Ring Height) [km]')
axes.set_title('Quantile Regression Plot: Peak Ring Height Vs Rim-crest Diameter')
plt.tight_layout()
plt.show()

