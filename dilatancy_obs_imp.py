import sys
import dilatancy_obs as do   #import the main script
import matplotlib.pyplot as plt

D = float(sys.argv[1])      #input the choice of rim-crest diameter in the command line
norm = bool(sys.argv[2])    #input norm as 'True' or 'False' in the command line depending on requirement

plt.figure()
plt.title('Radial Profile')
plt.xlabel('Rim Radius [km]')
plt.ylabel('Elevation [km]')
(x1,x2,x3),(y1,y2,y3) = do.lunar_crater_characteristics(D, plt, norm)
plt.legend()
plt.show()
