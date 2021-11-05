# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:32:27 2021

@author: hb1020
"""

from elements import *
from ray import *
import matplotlib.pyplot as plt, numpy as np

def spherical_refractor_test():    
    """
    Many-ray test for the SphericalRefractor class.
    """
    
    refractor = SphericalRefractor(10, (1/3), 1, 1.5, 2)
    
    rays = []
    results = []
    i = 0
    
    for y in range(-1, 2):
        for y_dir in range(-20, 21, 4):
            rays.append(Ray(np.array([0, y, 0]), np.array([0, y_dir / 10, 10])))
            i += 1
            
    
    for k, ray in enumerate(rays):
        refractor.propagate(ray)
        vertices = ray.vertices()
        vertices.append(vertices[-1] + 5 * ray.dirn())
        plt.plot([x[2] for x in vertices],[x[1] for x in vertices])
    
    plt.show()