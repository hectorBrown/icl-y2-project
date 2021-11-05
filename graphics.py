import matplotlib.pyplot as plt, numpy as np
import ray as r

def graph_zplane(rays, z):
    """
    Graphs a set of rays at a given z plane.
    """
    print(np.array([x.get_xy(z) for x in rays]).transpose())
    return plt.scatter(*np.array([x.get_xy(z) for x in rays]).transpose())