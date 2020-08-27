import numpy as np
import pySALEPlot as psp
from dilatancy_obs import lunar_crater_characteristics
import matplotlib.pyplot as plt
from scipy import optimize

model = psp.opendatfile('Dilatancy_moon45/jdata.dat', scale='km')  # open the data file of choice
x_mod, y_mod = model.surfaceProfile(500, returnx=True)  # get the simulations x and y values


def optimizer_function(x):
    """
    Optimising algorithm which outputs the rms_error and the best rim-crest diameter value
    for a given simulation
    :param x: Rim-crest diameter value
    :return: Root-mean square error
    """
    (x_obs, x2, x3), (y_obs, y2, y3) = lunar_crater_characteristics(x, norm=False, debug=False)
    sq_diff = (y_obs - y_mod) ** 2
    rms_error = np.sqrt(np.mean(sq_diff))
    return rms_error


o = optimize.minimize(optimizer_function, 25)
# starts from x=25 and finds the best fit
print(o)

#using the output x value from the optimiser, creates a plot of rms_error vs diameter
Ds = [20, 30, 46.6504, 50, 60, 70, 80]
errors = []

for D in Ds:
    (x_obs, x2, x3), (y_obs, y2, y3) = lunar_crater_characteristics(D, norm=False)
    sq_diff = (y_obs - y_mod) ** 2
    rms_error = np.sqrt(np.mean(sq_diff))
    print('The Root-mean squared error is:', rms_error)
    errors.append(rms_error)
plt.plot(Ds, errors, color='red')
plt.xlabel('Rim-crest Diameter [km]')
plt.ylabel('Rms Error')
plt.title('Rms error Vs Diameter')
plt.show()

#the commented code below can be used to create a plot of the model and observational profile
#by inputting the D value from the optimising algorithm

# D = 46.604
# (x_obs, x2, x3), (y_obs, y2, y3) = lunar_crater_characteristics(D, norm=False)
# sq_diff = (y_obs - y_mod) ** 2
# rms_error = np.sqrt(np.mean(sq_diff))
# plt.plot(x_obs, y_obs, color= 'magenta' ,label= 'Observation', )
# plt.plot(x_mod, y_mod, color= 'black', label= 'Model', )
# plt.legend()
# plt.xlabel('Diameter [km]')
# plt.ylabel('Elevation [km]')
# plt.show()

