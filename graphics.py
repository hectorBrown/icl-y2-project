# -*- coding: utf-8 -*-
"""
Graphics utility functions.

A bug in some versions of matplotlib will prevent these functions generating useful output for small values.
Update matplotlib to fix -- please see https://github.com/matplotlib/matplotlib/issues/6015.
"""

import matplotlib.pyplot as plt, numpy as np
import opticsutils as ou, elements as e

MPL_BUGFIX_SCALE = 1.1

def graph_zplane(rays, z):
    """
    Graphs a set of rays at a given z plane.
    """

    #a list of x,y values with those rays that don't pass z omitted
    xy = list(filter(lambda y : not y is None, [x.get_xy(z) for x in rays]))

    #check if there are any at all
    if len(xy):
        fig, ax = plt.subplots()
        ax.scatter(*np.array(xy).transpose())
        #attempted fix for matplotlib bug
        ax.set_xlim(-abs(max([x[0] for x in xy])) * MPL_BUGFIX_SCALE, abs(max([x[0] for x in xy])) * MPL_BUGFIX_SCALE)
        ax.set_ylim(-abs(max([x[1] for x in xy])) * MPL_BUGFIX_SCALE, abs(max([x[1] for x in xy])) * MPL_BUGFIX_SCALE)
        ax.set_aspect("equal")
        return fig
    else:
        raise Exception("None of the rays have positions for this z value.")

def graph_yplane(rays):
    """
    Graphs a set of rays as a y-z plane.
    """

    fig, ax = plt.subplots()
    for ray in rays:
        ax.plot([x[2] for x in ray.vertices()], [x[1] for x in ray.vertices()])
    return fig

def graph_spot_size(range, step, focus, z1, z2, n1, n2):
    """
    Graph RMS spot size (optimization measure) against curvature for a given range.

    range: should be a tuple (start, end).
    """
    c1 = np.arange(*range, step=step)
    size = []
    for i, c in enumerate(c1):
        print("{0:.1f}%".format(i / len(c1) * 100))
        if not ou.get_c2(c, focus) is None:
            size.append(ou.spot_size([e.SphericalRefractor(100e-3, c, 1, 1.5168),
                                    e.SphericalRefractor(105e-3, ou.get_c2(c, focus), 1.5168, 1)]))
        else:
            size.append(None)
    fig, ax = plt.subplots()
    ax.plot(c1, size)
    return fig
