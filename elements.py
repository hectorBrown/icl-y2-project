# -*- coding: utf-8 -*-
"""
Contains the Element base class, and all derived classes.
"""

import numpy as np, opticsutils as ou

class Element:
    def __str__(self):
        raise NotImplementedError()
    def __repr__(self):
        raise NotImplementedError()
    def propagate(self, ray):
        raise NotImplementedError()

class SphericalRefractor(Element):
    """
    Represents a spherical refracting surface.
    """
    def __init__(self, z0, curvature, n1, n2, apt):
        """
        z0: the intersection of the element with the z axis.
        curvature: 1/radius of curvature, this is negative if the centre of curvature is smaller than z0.
        n1: refractive index on the side facing negative z.
        n2: refractive index on the side facing positive z.
        apt: aperture radius.
        """
        self.__z0 = z0
        self.__curv = curvature
        self.__n1, self.__n2 = n1, n2
        self.__apt = apt
        
    def __repr__(self):
        return "elements.SphericalRefractor({:g}, {:g}, {:g}, {:g}, {:g})".format(self.__z0, self.__curv, self.__n1, self.__n2, self.__apt)

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
        
        #check if will intercept at all
        det = np.dot(r, ray.dirn())**2 - np.linalg.norm(r)**2 + (1/self.__curv)**2
        if det < 0:
            return None
        
        if self.__curv != 0:
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
        
        if np.sqrt(intercept[0]**2 + intercept[1]**2) > self.__apt:
            return None
        
        return intercept
        
    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, this method will return False, and won't update the ray.
        """
        intercept = self.__intercept(ray)
        
        if intercept is None:
            return False
        
        surface_normal = intercept - self.__center()
        surface_normal /= np.linalg.norm(surface_normal)
        
        ray.append(intercept, ou.refract(ray.dirn(), surface_normal, self.__n1, self.__n2))