import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import linregress

data = pd.read_csv("/Users/namya/Documents/Lunar_Data/diameter_peakdiam.csv")
data.head()

df = pd.DataFrame(data)
df.dropna(inplace=True)
df['log_Diam'] = np.log10(df['Diameter'])
df['log_peakdiam'] = np.log10(df['Peak Diam'])
print(df)
# print(df.var())    #function to calculate variance of diameter and depth
model = smf.quantreg('log_peakdiam ~ log_Diam', df)  # quantile regression plot
res = model.fit(q=.5)
print(res.summary())  # prints summary of the median quantile
quantiles = [0.5]
fits = [model.fit(q=q) for q in quantiles]
figure, axes = plt.subplots()
x = df['log_Diam']
y = df['log_peakdiam']
_x = np.linspace(x.min(), x.max(), num=len(y))  # range of x

_y_05 = fits[0].params['log_Diam'] * _x + fits[0].params['Intercept']
# start and end coordinates of fit lines
p = np.column_stack((x, y))

a__ = np.array([_x[0], _y_05[0]])  # first point of median line
b__ = np.array([_x[-1], _y_05[-1]])  # last point of median line

slope, intercept, r_value, p_value, std_err = linregress([_x[0], _x[-1]], [_y_05[0], _y_05[-1]])      #calculates the slope and intercept for the 0.9 quantile
print('median:',
      'slope:', "{:.4f}".format(slope), 'intercept:', "{:.4f}".format(intercept))
axes.scatter(x, df['log_peakdiam'], c='k', alpha=0.6, label='data points', )
axes.plot(_x, _y_05, label= 'median', c='r')
axes.legend()

axes.set_xlabel('log(Rim-crest Diameter) in km ')
axes.set_ylabel('log(Peak Ring Height) in km ')
axes.set_title('Quantile Regression Plot: Peak Ring Diameter Vs Rim-crest Diameter')
plt.tight_layout()
plt.show()

