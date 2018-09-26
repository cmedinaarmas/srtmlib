import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

# plot shaded heights
# mode: 'hsv', 'overlay', 'soft'
def shade(heights, filename, az=90, alt=45, ve=1, mode=None,cmap='jet'):
    ls = LightSource(azdeg=az, altdeg=alt)
    sizes = np.shape(heights)
    height = float(sizes[0])
    width  = float(sizes[1])

    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    if mode == None:
        # plot hillshade intensity image
        shaded = ls.hillshade(heights.astype('float'), vert_exag=ve)
        ax.imshow(shaded, cmap='gray')
        plt.savefig(filename, dpi = height) 

    else:
        #blend hillshaded intensity
        rgb = ls.shade(heights.astype('float'), cmap=cmap, blend_mode=mode,vert_exag=ve)

        ax.imshow(rgb)
        plt.savefig(filename, dpi = height) 
 


# plot raw heights
def plot(heights, filename, cmap='gray'):
    sizes = np.shape(heights)
    height = float(sizes[0])
    width = float(sizes[1])

    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(heights, cmap=cmap)
    plt.savefig(filename, dpi = height) 

    fig = plt.figure() 
