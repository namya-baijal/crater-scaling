import pySALEPlot as psp
from pylab import figure, arange, colorbar, loadtxt, figtext
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from dilatancy_obs import lunar_crater_characteristics
import sys

D = float(sys.argv[1])  #use the best fit D value from the optimiser in error_script.py

# Make an output directory
dirname = 'Plots_moon45'
psp.mkdir_p(dirname)

# Specify the set of simulations to process
simulations = ["Dilatancy_moon45"]
# Plot title (should be same length as "simualtions")
ptitle = ["$L$ = 3.2 km; $v_i$ = 15 km/s; $g$ = 1.62 m/s$^2$"]
# x-limit of the plot (should be same length as "simulations")
xmax = [32.]

n = 0
for sim in simulations:

    # Define datafilename
    datafilename = sim + '/jdata.dat'

    # Open the datafile
    model = psp.opendatfile(datafilename)

    # Set the distance units to km
    model.setScale('km')

    # If a single image with no gravity profile, create a simple single axes figure.
    fig = figure(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 1)
    ax = fig.add_subplot(gs[0], aspect='equal')

    steps = arange(0, model.nsteps, 20)
    for index, i in enumerate(steps):  # every 10 time steps

        # Set the axis labels
        ax.set_xlabel('r [km]')
        ax.set_ylabel('z [km]')
        ax.set_title(ptitle[n])

        # Set the axis limits
        ax.set_xlim([0, xmax[n]])
        ax.set_ylim([-xmax[n] / 2., xmax[n] / 5.])

        # Read the step
        step = model.readStep('Alp', i)

        print('Processing step: ', i)

        # Plot the distension field as porosity as a colourmap (original colour= binary)
        p = ax.pcolormesh(model.x, model.y, 1. - 1. / step.data[0],
                          cmap='binary', vmin=0., vmax=0.2)

        # And the material boundary
        b = ax.contour(model.xc, model.yc, step.cmc[0], colors='k', levels=[0.1])
        c = ax.contour(model.xc, model.yc, step.cmc[1], colors='k', levels=[0.1])

        # Add a colorbar (only need to do this once)
        if (i == 0):  # only for the first time step
            cb = fig.colorbar(p, orientation='horizontal', shrink=0.8, pad=0.15)
            cb.set_label('Porosity')
            # Add a tracer overlay
        for u in range(model.tracer_numu):
            tru = model.tru[u]
            for l in arange(0, len(tru.xlines), 10):  # Plot the tracers in horizontal lines, every 10 lines
                ax.plot(step.xmark[tru.xlines[l]],
                        step.ymark[tru.xlines[l]],
                        c='k', marker='.', linestyle='None', markersize=0.25)
                for l in arange(0, len(tru.ylines), 10):  # plot the tracers in vertical lines, every 10 lines
                    ax.plot(step.xmark[tru.ylines[l]],
                            step.ymark[tru.ylines[l]],
                            c='k', marker='.', linestyle='None', markersize=0.25)

        # Add time labels to the frames
        ax.annotate('T = {: 3.0f} s'.format(step.time), xy=(0.775 * xmax[n], xmax[n] / 6.), xycoords='data',
                    horizontalalignment='left', verticalalignment='top')

        if (index == len(steps) - 1):   #on the last time step, overlays the observational radial profile
            lunar_crater_characteristics(D, ax, norm= False)
            ax.legend()
        # Save the figure if one per simulation
        fig.savefig('./{}/{}-{:05d}.png'.format(dirname, sim, i), dpi=300)

        # Remove the field, ready for the next timestep to be plotted
        ax.cla()

    n = n + 1
    profile, metrics = model.surfaceProfile(500, metrics=True, rimrad=True)


