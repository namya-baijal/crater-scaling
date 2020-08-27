#Run this script from within Dilatancy_moon45 to create a mirror plot of the two simulations

import pySALEPlot as psp
from pylab import figure, arange, colorbar, loadtxt, figtext
# This allows the figure to be subdivided non-uniformly
from matplotlib import gridspec
# Need this for the colorbars we will make on the mirrored plot
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Make an output directory
dirname = 'Compare_moon_models'
psp.mkdir_p(dirname)

# Specify the set of simulations to process
simulations = ['Dilatancy_moon45', 'Dilatancy_moon46']

# Plot title (should be same length as "simualtions")
ptitle = ["$L$ = 3.2 km; $v_i$ = 15 km/s;Moon:$g$ = 1.62 m/s$^2$;"]

# x-limit of the plot (should be same length as "simulations")
xmax = [32.]

n = 0

# Define datafilename
datafilename1 = simulations[0] + '/jdata.dat'
datafilename2 = simulations[1] + '/jdata.dat'

# Open the datafiles
model1 = psp.opendatfile(datafilename1)
model2 = psp.opendatfile(datafilename2)

# Set the distance units to km
[model.setScale('km') for model in [model1, model2]]

# If a single image with no gravity profile, create a simple single axes figure.
fig = figure(figsize=(8, 6))
gs = gridspec.GridSpec(1, 1)
ax = fig.add_subplot(gs[0], aspect='equal')

for i in arange(0, model1.nsteps, 10):  # every 10 time steps

    # Set the axis labels
    ax.set_xlabel('r [km]')
    ax.set_ylabel('z [km]')
    ax.set_title(ptitle[n], loc='center')

    # Set the axis limits
    ax.set_xlim([-xmax[0], xmax[0]])
    ax.set_ylim([-xmax[n] / 2., xmax[n] / 5.])

    # Read the step
    step1 = model1.readStep('Alp', i)
    step2 = model2.readStep('Alp', i)

    print('Processing step: ', i)

    # Plot the distension field as porosity as a colourmap
    p = ax.pcolormesh(model1.x, model1.y, 1. - 1. / step1.data[0],
                      cmap='Blues', vmin=0., vmax=0.2)
    q = ax.pcolormesh(-model2.x, model2.y, 1. - 1. / step2.data[0],
                      cmap='Blues', vmin=0., vmax=0.2)

    # And the material boundary
    b = ax.contour(model1.xc, model1.yc, step1.cmc[0], colors='k', levels=[0.1])
    c = ax.contour(model1.xc, model1.yc, step1.cmc[1], colors='k', levels=[0.1])

    d = ax.contour(-model2.xc, model2.yc, step2.cmc[0], colors='k', levels=[0.1])
    e = ax.contour(-model2.xc, model2.yc, step2.cmc[1], colors='k', levels=[0.1])

    #add the colourbar for porosity

    if (i == 0):
        cb1 = fig.colorbar(p, orientation='horizontal', shrink=0.8, pad=0.15)
        cb1.set_label('Porosity')

    for u in range(model1.tracer_numu):
        tru = model1.tru[u]
        for l in arange(0, len(tru.xlines), 10):  # Plot the tracers in horizontal lines, every 10 lines
            ax.plot(step1.xmark[tru.xlines[l]],
                    step1.ymark[tru.xlines[l]],
                    c='k', marker='.', linestyle='None', markersize=0.25)
            for l in arange(0, len(tru.ylines), 10):  # plot the tracers in vertical lines, every 10 lines
                ax.plot(step1.xmark[tru.ylines[l]],
                        step1.ymark[tru.ylines[l]],
                        c='k', marker='.', linestyle='None', markersize=0.25)
    for u in range(model2.tracer_numu):
        tru = model2.tru[u]
        for l in arange(0, len(tru.xlines), 10):  # Plot the tracers in horizontal lines, every 10 lines
            ax.plot(-step2.xmark[tru.xlines[l]],
                    step2.ymark[tru.xlines[l]],
                    c='k', marker='.', linestyle='None', markersize=0.25)
            for l in arange(0, len(tru.ylines), 10):  # plot the tracers in vertical lines, every 10 lines
                ax.plot(-step2.xmark[tru.ylines[l]],
                        step2.ymark[tru.ylines[l]],
                        c='k', marker='.', linestyle='None', markersize=0.25)

    # Add time labels to the frames
    ax.annotate('T = {: 3.0f} s'.format(step1.time), xy=(0.775 * xmax[n], xmax[n] / 6.), xycoords='data',
                horizontalalignment='left', verticalalignment='top')

    # Save the figure if one per simulation
    fig.savefig('./{}/{}-{:05d}.png'.format(dirname, simulations[0], i), dpi=300)

    # Remove the field, ready for the next timestep to be plotted
    ax.cla()

n = n + 1
