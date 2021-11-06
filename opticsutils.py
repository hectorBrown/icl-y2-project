# -*- coding: utf-8 -*-
"""
General purpose utility functions for optics.
"""

import numpy as np

def refract(incident, surface, n1, n2):
    """
    Refracts a ray according to Snell's law, both incident and surface should be normalised vectors.
    """

    #get angle of incidence
    the_1 = np.arccos(np.dot(-incident, surface))
    
    if np.sin(the_1) > (n2/n1):
        #if TIR
        return None
    
    #calc angle of refraction
    the_2 = np.arcsin((n1/n2) * np.sin(the_1))
    
    if the_2 == 0:
        return -surface
    
    #find refracted ray in plane - this uses the fact that the refracted ray will be a linear combination of the surface and incident rays
    b = abs(np.sin(the_2)/np.sin(the_1))
    a = b * np.cos(the_1) - np.cos(the_2)
    refracted = a * surface + b * incident
    
    return refracted