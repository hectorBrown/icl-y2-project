# -*- coding: utf-8 -*-
"""
Contains the Element base class, and all derived classes.
"""

import numpy as np
import opticsutils as ou

class Element:

    def __repr__(self):
        raise NotImplementedError()

    def propagate(self, ray):
        raise NotImplementedError()

class SphericalRefractor(Element):
    """
    Represents a spherical refracting surface.
    """

    def __init__(self, z0, curvature, n1, n2, apt=None):
        """
        z0: the intersection of the element with the z axis.
        curvature: 1/radius of curvature, this is negative if the centre of curvature is smaller than z0.
        n1: refractive index on the side facing negative z.
        n2: refractive index on the side facing positive z.
        Both n1, n2 can be functions of wavelengths, or constant values. If functions, they should be able to handle and provide output for input None.
        apt: aperture radius.
        """

        self.__z0 = z0
        self.__curv = curvature

        if callable(n1):
            self.__n1 = n1
        else:
            self.__n1 = lambda x : n1
        if callable(n2):
            self.__n2 = n2
        else:
            self.__n2 = lambda x : n2

        self.__apt = apt
        
    def __repr__(self):
        if not self.__apt is None:
            return "elements.SphericalRefractor({:g}, {:g}, {}, {}, {:g})".format(self.__z0, self.__curv, self.__n1, self.__n2, self.__apt)
        else:
            return "elements.SphericalRefractor({:g}, {:g}, {}, {})".format(self.__z0, self.__curv, self.__n1, self.__n2)

    def __center(self):
        """
        Gets the center of curvature of the lens.
        """
        
        if self.__curv != 0:
            return np.array([0, 0, self.__z0 + (1/self.__curv)])
        else:
            return np.array([0, 0, self.__z0])
    
    def __intercept(self, ray):
        """
        Calculates the first intercept of a ray with the surface described.
        """
        
        #vector difference between centre of curvature and ray position
        r = ray.pos() - self.__center()
        l = None
    
        
        if self.__curv != 0:
            #check if will intercept at all
            det = np.dot(r, ray.dirn())**2 - np.linalg.norm(r)**2 + (1/self.__curv)**2
            if det < 0:
                return None
            
            #calculate the two intersections with the sphere
            a = -np.dot(r, ray.dirn())
            b = np.sqrt(det)
            
            #select based on curvature
            if self.__curv < 0:
                l = a + b
            else:
                l = a - b
        else:
            #special case for a planar surface
            l = (self.__z0 - ray.pos()[2]) / ray.dirn()[2]

        #check if intersection behind
        if l < 0:
            return None
        
        #check if point of intersection lies outside apt
        intercept = ray.pos() + l * ray.dirn()
        if not self.__apt is None:
            if np.sqrt(intercept[0]**2 + intercept[1]**2) > self.__apt:
                return None
        
        return intercept

    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, or totally internally reflects, this method will return False, and won't update the ray.
        """

        intercept = self.__intercept(ray)
        
        if intercept is None:
            return False
        
        if self.__curv > 0:
            surface_normal = intercept - self.__center()
        elif self.__curv < 0:
            surface_normal = self.__center() - intercept
        else:
            surface_normal = np.array([0,0,-1.0])
            
        surface_normal /= np.linalg.norm(surface_normal)

        refracted_dirn = ou.refract(ray.dirn(), surface_normal, self.__n1(ray.wavelength()), self.__n2(ray.wavelength()))

        if not refracted_dirn is None:
            ray.append(intercept, refracted_dirn)
        else:
            return False
        
class OutputPlane(Element):
    """
    Represents a virtual plane that does not modify rays.
    """

    def __init__(self, z0):
        """
        z0: the intersection of the element with the z axis.
        """

        self.__z0 = z0

    def __repr__(self):
        return "elements.OutputPlane({:g})".format(self.__z0)
    

    def __intercept(self, ray):
        l = (self.__z0 - ray.pos()[2]) / ray.dirn()[2]
        
        #check if behind
        if l < 0:
            return None
    
        intercept = ray.pos() + l * ray.dirn()
        
        return intercept
    

    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, this method will return False, and won't update the ray.
        """

        intercept = self.__intercept(ray)
        
        if intercept is None:
            return False
        
        ray.append(intercept, ray.dirn().copy())
