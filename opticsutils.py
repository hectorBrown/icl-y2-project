# -*- coding: utf-8 -*-
"""
General purpose utility functions for optics.
"""

import numpy as np, scipy.optimize as op, os.path as osp
import ray as r, elements as e

visible_lims = (380e-9, 740e-9)

def refract(incident, surface, n1, n2):
    """
    Refracts a ray according to Snell's law, both incident and surface should be normalised vectors.
    """

    #get angle of incidence
    the_1 = np.arccos(np.dot(-incident, surface))

    if np.sin(the_1) > (n2/n1):
        #TIR
        return reflect(incident, surface)
    
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

def get_focus(sys, paraxial_precision=None, output_step=250e-3):
    """
    Uses a probe ray to estimate the focal point of an optical system.
    paraxial_precision: the y-height of the probe ray.
    output_step: best not to change, effects the way the function iterates, try raising if not producing output.
    
    Returns the z-value of the paraxial focus, or false if the system does not converge.
    """
    if paraxial_precision is None:
        paraxial_precision = sys.get_paraxial()
    
    probe = r.Ray([0, paraxial_precision, 0], [0,0,1])
    sys.propagate(probe)
    
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
    
def spot_size(sys, focus=None, bundle_radius=5e-3):
    """
    Gets the RMS geometrical spot size for a system.
    focus: defaults to None, if None will use opticsutils.get_focus to find.
    bundle_radius: the radius of the bundle used for estimation.
    
    If this method hangs, it is likely due to opticsutils.get_focus - call it explicitly as a kwarg to adjust running parameters or input a focus manually.
    Returns false if the system does not converge.
    """
    
    if focus is None:
        focus = get_focus(sys)
        if not focus:
            return False
        
    bundle = r.bundle(bundle_radius, 6, 6)
    #coefficient because sometimes focus is truncated between here and get_xy, and the focal point lies past the output plane
    sys.append(e.OutputPlane(focus * 1.1))
    
    sys.propagate(bundle)
    
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
        return op.newton(lambda x : get_focus(e.System(elements=[e.SphericalRefractor(z1, c1, n1, n2),
                                                e.SphericalRefractor(z2, x, n2, n1)])) - focus, guess)
    except:
        return None

def load_index(path):
    """
    Returns a lookup table of wavelength:index pairs from a CSV.

    e.g.
    ---material.csv---
    wavelength_1,index_1
    wavelength_2,index_2
    wavelength_3,index_3
    ...
    ------------------

    Path should be relative.
    """
    
    return {x[0]:x[1] for x in np.loadtxt(osp.join(osp.abspath(osp.dirname(__file__)), path), delimiter=',')}
    

def get_index(table, wavelength):
    """
    Returns the index of an arbitrary index from a lookup table.
    """
    
    sorted_keys = sorted(table.keys())
    
    if wavelength < sorted_keys[0] or wavelength > sorted_keys[-1]:
        raise ValueError("No value for given wavelength in the range of the table.")
    
    for i in range(len(sorted_keys) - 1):
        pair = (sorted_keys[i], sorted_keys[i+1])
        if wavelength >= pair[0] and wavelength <= pair[1]:
            grad = (table[pair[1]] - table[pair[0]]) / (pair[1] - pair[0])
            return table[pair[0]] + grad * (wavelength - pair[0])
    