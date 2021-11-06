# -*- coding: utf-8 -*-
"""
Graphics utility functions.
"""

import matplotlib.pyplot as plt, numpy as np
import ray as r

def graph_zplane(rays, z):
    """
    Graphs a set of rays at a given z plane.
    """
    #THIS DOESN'T WORK?
    xy = list(filter(lambda y : not y is None, [x.get_xy(z) for x in rays]))
    if len(xy):
        fig = plt.figure()
        plt.scatter(*np.array(xy).transpose())
        return fig
    else:
        raise Exception("None of the rays have positions for this z value.")

def graph_yplane(rays):
    """
    Graphs a set of rays as a y-z plane.
    """
    fig = plt.figure()
    for ray in rays:
        plt.plot([x[2] for x in ray.vertices()], [x[1] for x in ray.vertices()])
    return fig