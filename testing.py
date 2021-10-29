# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:32:27 2021

@author: hb1020
"""

from elements import *
from ray import *

def spherical_refractor_test():    
    """
    Many-ray test for the SphericalRefractor class.
    """
    
    refractor = SphericalRefractor(10, (1/3), 1, 1.5, 2)
    
    rays = []
    results = []
    i = 0
    
    for x in range(0, 20, 4):
        for y in range(0, 20, 4):
            rays.append(Ray(np.array([x / 10, y / 10, 0]), np.array([0, 0, 10])))
            results.append([rays[i].copy()])
            i += 1
    
    #generates error
#    for x in range(0, 20, 4):
#        for y in range(0, 20, 4):
#            for x_dir in range(-20, 20, 4):
#                for y_dir in range(-20, 20, 4):
#                    rays.append(Ray(np.array([x / 10, y / 10, 0]), np.array([x_dir / 10, y_dir / 10, 10])))
#                    results.append([rays[i].copy()])
#                    i += 1
    
    for k, ray in enumerate(rays):
        refractor.propagate(ray)
        results[k].append(ray.copy())
    
    return results