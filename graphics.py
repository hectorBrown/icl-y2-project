# -*- coding: utf-8 -*-
"""
Graphics utility functions.

A bug in some versions of matplotlib will prevent these functions generating useful output for small values.
Update matplotlib to fix -- please see https://github.com/matplotlib/matplotlib/issues/6015.
"""

import matplotlib.pyplot as plt, numpy as np
import ray as r

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
        ax.set_xlim(-abs(max([x[0] for x in xy])) * 1.1, abs(max([x[0] for x in xy])) * 1.1)
        ax.set_ylim(-abs(max([x[1] for x in xy])) * 1.1, abs(max([x[1] for x in xy])) * 1.1)
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
