import numpy as np

import pySALEPlot as psp


def H_u(D):  # upper limit crater_depth from baker
    return (10 ** 0.3043) * (D ** 0.1946)


def H_l(D):  # lower limit crater depth from baker
    return (10 ** 0.4717) * (D ** 0.0291)


def H(D):  # function to calculate median crater depth from baker
    return (10 ** 0.2913) * (D ** 0.1684)


def Df(D):  # function to calculate crater floor diameter
    if D >= 20 and D <= 480:
        Df = 0.187 * (D ** 1.249)
        return Df
    else:
        raise ValueError('Crater Floor Diameter: Not calculable for input D value')


def Dcp(D):
    if D >= 20 and D <= 140:  # equation to calculate central peak diameter from pike
        return 0.22 * D
    elif D > 140 and D <= 450:  # equation to calculate peak ring diameter from baker
        return (10 ** (-0.7744)) * (D ** 1.1808)
    else:
        raise ValueError('Peak Diameter: Not calculable for input D value')


def hcp(D):  # function to calculate central peak height or peak ring height from baker paper
    if D <= 205:
        return (10 ** (-1.7004)) * (D ** 0.8939)
    elif D > 205 and D <= 450:  # peak ring height equation from insufficient data points (8)
        return (10 ** (-3.3722)) * (D ** 1.4468)
    else:
        raise ValueError('Central Peak Height: Not calculable for input D value')


def hcp_U(D):  # function to calculate upper limit central peak height and peak ring height from baker paper
    if D <= 205:  # upper central peak height
        return (10 ** (-1.003)) * (D ** 0.6516)
    elif D > 205 and D <= 450:  # upper peak ring height (only 8 data points available)
        return (10 ** (-4.0160)) * (D ** 1.7774)
    else:
        raise ValueError('Central Peak Height: Not calculable for input D value')


def hcp_L(D):  # function to calculate lower limit central peak height from baker paper
    if D <= 205:  # lower central peak height
        return (10 ** (-2.1490)) * (D ** 0.9426)
    elif D > 205 and D <= 450:  # lower peak ring height
        return (10 ** (-4.4175)) * (D ** 1.8219)
    else:
        raise ValueError('Central Peak Height: Not calculable for input D value')


def hr(D):  # Function to calculate rim height from Melosh textbook
    if D < 21:
        return 0.036 * (D ** 1.014)
    elif D >= 21 and D <= 400:
        return 0.236 * (D ** 0.399)
    else:
        raise ValueError('Rim Height: Not calculable for input D value')


def hr_U(D):  # upper rim height
    u_factor = H_u(D) / H(D)  # find the upper limit factor by dividing upper limit crater depth by median crater depth
    return u_factor * hr(D)  # multiply factor by the median rim height to get upper limit rim height


def hr_L(D):  # lower rim height
    l_factor = H_l(D) / H(D)  # find the lower limit factor by dividing lower limit crater depth by median crater depth
    return l_factor * hr(D)  # multiply factor by the median rim height to get lower limit rim height


def Wt(D):  # function to calculate terrace zone width from Melosh textbook
    if D >= 15 and D <= 350:
        return 0.92 * (D ** 0.67)
    else:
        raise ValueError('Terrace Zone Width: Not calculable for input D value')


def w(D):  # function to calculate widest terrace width from Melosh textbook
    if D >= 20 and D <= 200:
        return 0.09 * (D ** 0.87)
    else:
        raise ValueError('Widest Terrace Width: Not calculable for input D value')


model = psp.opendatfile('Dilatancy_moon45/jdata.dat', scale='km')   #open the required data file
x_mod, y_mod = model.surfaceProfile(500, returnx=True)              #generates array of x ,y values from the simulation


def crater_radial_profile(rim_rad, peak_diam, crater_floor_diam, crater_depth,
                          peak_height, rim_height, norm=False, x_in=x_mod):
    """
    This is the base function that creates a radial profile using the lunar crater parameters.
    Call this function in lunar_crater_characteristics.
    :param rim_rad: Rim radius of the impact crater based on input D value
    :param peak_diam: Diameter of the central peak/ peak ring based on input D value including upper and lower limits
    :param crater_floor_diam: Diameter of crater floor based on input D value
    :param crater_depth: Depth of impact crater including upper and lower limits
    :param peak_height: Height of central peak / peak ring based on input D value including upper and lower limits
    :param rim_height: Height of the crater rim based on input D value including
    :param norm : if True,generates a list of normalised radii values along the radial profile for plotting instead of unnormalised radii values

    :return: x: Rim-radius of the crater profile
             y: Elevation of the profile

    """

    r_norm = np.arange(0., 3.01, 0.01)  # generates 300 points along the radial profile 'normalised radius'
    if norm == True:
        x = r_norm * rim_rad  # multiply the normalised radial points with the rim-crest radius of
    else:
        x = x_in

    y = np.zeros_like(x)  # generate an array of elevation points = radial points
    central_peak_rad = peak_diam / 2  # central peak radius = peak diameter / 2
    floor_radius = crater_floor_diam / 2  # crater floor radius = crater floor diameter /2
    rim_slope = ((crater_depth)) / (rim_rad - floor_radius)  # rim slope = y/x2 - x1
    peak_slope = (peak_height) / (-central_peak_rad)  # peak slope = y / x
    correction2 = peak_height + rim_height - crater_depth  # to bring the point from peak height down to the crater depth
    correction1 = ((rim_slope * floor_radius) - (
            rim_height - crater_depth))  # to correct for the rim slope to start from crater depth and go up to rim height
    for i in np.arange(len(x)):
        if x[i] <= central_peak_rad:  # if (inside peak):
            y[i] = ((peak_slope * x[i]) + correction2)  # equation for calculating the slope of peak

        elif x[i] <= floor_radius:  # if (inside floor) :
            y[
                i] = -crater_depth + rim_height  # equation to calculate the crater depth (corrected for removing rim height because it already includes that)

        elif x[i] <= rim_rad:  # if (inside rim) :
            y[i] = ((rim_slope * x[i]) - correction1)  # equation to calculate the rim slope
        else:  # else:
            y[i] = rim_height * ((x[i] / rim_rad) ** -3)  # calculates the ejecta thickness
    return x, y


def lunar_crater_characteristics(D, plt=None, norm=True, debug=True):
    """
    Calculates lunar crater dimensions as a function of input rim-diameter.

        Creates 3 radial profiles- Upper limit, Lower limit and
        median depending on the input norm (normalised or
        unnormalised array of radii values) which can be then compared
        with the iSALE simulations
        :param D: Rim-crest Diameter. Insert the estimated value in the command line.
        :param plt: Plotting parameter to create the plots of the radial profile
        :param norm: inputting "True" in the command line returns the array of normalised radii values.
        "False" returns unnormalised values.
        :param debug: If set to 'True' it prints all the lunar crater metrics

    """

    if D > 582:  # maximum value of input diameter from the data set
        raise ValueError('Diameter must be less than 582 km')

    if debug:
        print('**********Lunar Crater Morphometry**********')
        print('Rim-Rim Diameter:', D, 'km')

    crater_depth = H(D)
    if debug:
        print('Crater Depth:', "{:.2f}".format(-crater_depth), 'km')

    upper_crater_depth = H_u(D)
    if debug:
        print('Upper Limit Crater Depth:', "{:.2f}".format(-upper_crater_depth), 'km')

    lower_crater_depth = H_l(D)
    if debug:
        print('Lower Limit Crater Depth:', "{:.2f}".format(-lower_crater_depth), 'km')

    try:
        crater_floor_diam = Df(D)
        if debug:
            print('Crater Floor Diameter:', "{:.2f}".format(crater_floor_diam), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass

    try:
        central_peak_diam = Dcp(D)
        if debug:
            print('Central Peak Diameter:', "{:.2f}".format(central_peak_diam), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass
    try:
        central_peak_height = hcp(D)
        if debug:
            print('Central Peak Height:', "{:.2f}".format(central_peak_height), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass
    try:
        upper_peak_height = hcp_U(D)
        if debug:
            print('Upper Peak Height:', "{:.2f}".format(upper_peak_height), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass
    try:
        lower_peak_height = hcp_L(D)
        if debug:
            print('Lower Peak Height:', "{:.2f}".format(lower_peak_height), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass

    try:
        rim_height = hr(D)
        if debug:
            print('Rim Height:', "{:.2f}".format(rim_height), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass

    upper_rim_height = hr_U(D)
    if debug:
        print('Upper Rim Height:', "{:.2f}".format(upper_rim_height), 'km')

    lower_rim_height = hr_L(D)
    if debug:
        print('Lower Rim Height:', "{:.2f}".format(lower_rim_height), 'km')

    try:
        terrace_zone_width = Wt(D)
        if debug:
            print('Terrace Zone Width:', "{:.2f}".format(terrace_zone_width), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
        pass

    try:
        widest_terrace_width = w(D)
        if debug:
            print('Widest Terrace Width:', "{:.2f}".format(widest_terrace_width), 'km')
    except ValueError as e:
        if debug:
            print(str(e))
            pass

    if debug:
        print('**********************************************')

    rim_rad = D / 2  # rim radius = rim crest diameter / 2

    x1, y1 = crater_radial_profile(rim_rad, central_peak_diam, crater_floor_diam, crater_depth,
                                   central_peak_height, rim_height, norm=norm)
    x2, y2 = crater_radial_profile(rim_rad, central_peak_diam, crater_floor_diam, lower_crater_depth,
                                   upper_peak_height, upper_rim_height, norm=norm)
    x3, y3 = crater_radial_profile(rim_rad, central_peak_diam, crater_floor_diam, upper_crater_depth,
                                   lower_peak_height, lower_rim_height, norm=norm)
    if plt:
        plt.plot(x1, y1, color='magenta', label='Median')  # plots the median profile
        plt.plot(x2, y2, color='blue', dashes=[6, 2], label='Upper Limit')  # plots upper limit profile
        plt.plot(x3, y3, color='green', dashes=[6, 2], label='Lower Limit')  # plots lower limit profile

    return (x1, x2, x3), (y1, y2, y3)
