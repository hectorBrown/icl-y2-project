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
    
    #find refracted ray in plane
    b = (np.cos(the_1) * np.cos(the_2) + np.sqrt((np.cos(the_1) * np.cos(the_2))**2 + 4 * np.sin(the_2)**2))/2
    a = np.cos(the_2) - b * np.cos(the_1)
    refracted = -a * surface + b * incident
    
    #return
    return refracted