# -*- coding: utf-8 -*-
"""
General purpose utility functions for optics.
"""

import numpy as np, scipy.optimize as op
import ray as r, elements as e

#a value that tries to account for the truncation of numbers in the spot_size() method
__SPOTSIZE_OUTPUT_ERROR=1.1

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

def reflect(incident, surface):
    """
    Reflects a ray, both incident and surface should be normalised vectors.
    """

    #get angle of incidence
    the = np.arccos(np.dot(-incident, surface))

    reflected = incident + np.sqrt(2 * (1 - np.cos(np.pi - 2 * the))) * surface

    return reflected

def get_focus(system, paraxial_precision=0.1e-3, output_step=250e-3):
    """
    Uses a probe ray to estimate the focal point of an optical system.
    system: should be a list containing all surfaces.
    paraxial_precision: the y-height of the probe ray.
    output_step: best not to change, effects the way the function iterates, try raising if not producing output.
    
    Returns the z-value of the paraxial focus, or false if the system does not converge.
    """
    
    probe = r.Ray([0, paraxial_precision, 0], [0,0,1])
    for surface in lens:
        surface.propagate(probe)
    
    #return False if lens doesn't focus
    e.OutputPlane(output_step).propagate(probe)
    if probe.vertices()[-1][1] >= probe.vertices()[-2][1]:
        return False

    #this progressively increases the output plane until the probe ray falls through the z-axis.
    i = 2
    while probe.pos()[1] > 0:
        output = e.OutputPlane(i * output_step * probe.dirn()[2]/abs(probe.dirn()[2]))
        output.propagate(probe)
        i += 1
    
    #assuming linear ray propagation, interpolates z position
    vertices = probe.vertices()
    ratio = abs(vertices[-2][1]/(vertices[-2][1] - vertices[-1][1]))
    
    return (vertices[-1][2] - vertices[-2][2]) * ratio + vertices[-2][2]
    
def spot_size(system, focus=None, bundle_radius=5e-3):
    """
    Gets the RMS geometrical spot size for a system.
    focus: defaults to None, if None will use opticsutils.get_focus to find.
    bundle_radius: the radius of the bundle used for estimation.
    
    If this method hangs, it is likely due to opticsutils.get_focus - call it explicitly as a kwarg to adjust running parameters or input a focus manually.
    Returns false if the system does not converge.
    """
    
    if focus is None:
        focus = get_focus(system)
        if not focus:
            return False
        
    bundle = r.bundle(bundle_radius, 6, 6)
    output = e.OutputPlane(focus * __SPOTSIZE_OUTPUT_ERROR)
    
    for ray in bundle:
        for surface in system:
            surface.propagate(ray)
        output.propagate(ray)
    
    spots = [np.linalg.norm(r.get_xy(focus))**2 for r in bundle]
    
    return np.sqrt(np.average(spots))
            
def get_c2(c1, focus, z1=100e-3, z2=105e-3, n1=1, n2=1.5168):
    """
    Finds the curvature c2 of a surface in a singlet lens for a given focus.

    c1: curvature of the first surface.
    focus: paraxial focus point.
    z1: position of the first lens.
    z2: position of the second lens.
    n1: refractive index of the environment.
    n2: refractive index of the lens.
    """
    try:
        #guess from the lens maker's formula
        guess = c1 - ((focus - z1) * (n2 - n1))**-1
        return op.newton(lambda x : get_focus([e.SphericalRefractor(z1, c1, n1, n2),
                                                e.SphericalRefractor(z2, x, n2, n1)]) - focus, guess)
    except:
        return None
