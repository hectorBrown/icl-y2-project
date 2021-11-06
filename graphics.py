import matplotlib.pyplot as plt, numpy as np
import ray as r

def graph_zplane(rays, z):
    """
    Graphs a set of rays at a given z plane.
    """
    #THIS DOESN'T WORK?
    fig = plt.figure()
    plt.scatter(*np.array([x.get_xy(z) for x in rays]).transpose())
    return fig

def graph_yplane(rays):
    fig = plt.figure()
    for ray in rays:
        plt.plot([x[2] for x in ray.vertices()], [x[1] for x in ray.vertices()])
    return fig
