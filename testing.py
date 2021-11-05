# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:32:27 2021

@author: hb1020
"""

import elements as e, ray as r
import matplotlib.pyplot as plt, numpy as np

def spherical_refractor(z0, curvature, n1, n2, output_z0):
    refractor = e.SphericalRefractor(z0, curvature, n1, n2, 1/curvature)
    output = e.OutputPlane(output_z0)
    
    rays = []
    
    #setup rays
#    for i in range(6):
#        for j in range(-5, 6):
#            y = i * 2 * z0 / 10
#            y_dir = j * 2 * z0 / 10
#            
#            rays.append(r.Ray(np.array([0, y, 0]), np.array([0, y_dir, z0])))
    
    rays.append(r.Ray(np.array([0, 0.1, 0]), np.array([0, 0, 1])))
    rays.append(r.Ray(np.array([0, 0, 0]), np.array([0, 0, 1])))
    rays.append(r.Ray(np.array([0, 0.2, 0]), np.array([0, 0, 1])))
    
    #propagate through system
    for ray in rays:
        refractor.propagate(ray)
        output.propagate(ray)
        plt.plot([x[2] for x in ray.vertices()], [x[1] for x in ray.vertices()])
    
    plt.show()
    
