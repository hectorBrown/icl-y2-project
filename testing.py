# -*- coding: utf-8 -*-
"""
Testing module.
"""

import matplotlib.pyplot as plt, numpy as np
import elements as e, ray as r

def spherical_refractor(z0, curvature, n1, n2, output_z0):
    """
    A relatively generic spherical refractor test.
    """

    refractor = e.SphericalRefractor(z0, curvature, n1, n2, 1/curvature)
    output = e.OutputPlane(output_z0)
    
    rays = []
    
    #setup rays in 2 directions
    for i in range(6):
        y = i * (1/curvature) / 10
        
        rays.append(r.Ray(np.array([0, y, 0]), np.array([0, 0, z0])))
    
    for i in range(6):
        y = i * (1/curvature) / 10
        
        rays.append(r.Ray(np.array([0, y, 0]), np.array([0, -(1/curvature) / 10, z0])))

    #propagate through system
    for ray in rays:
        refractor.propagate(ray)
        output.propagate(ray)
        plt.plot([x[2] for x in ray.vertices()], [x[1] for x in ray.vertices()])
    
    plt.show()