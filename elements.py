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
    
    def get_paraxial(self):
        raise NotImplementedError()

class SphericalElement(Element):
    """
    Abstract spherical element base class.
    """

    def __init__(self, z0, curvature, apt):
        self._z0, self._curv, self._apt = z0, curvature, apt

    def _center(self):
        """
        Gets the center of curvature of the element.
        """
        if self._curv != 0:
            return np.array([0, 0, self._z0 + (1/self._curv)])
        else:
            return np.array([0, 0, self._z0])

    def get_paraxial(self):
        """
        Gets a number indicative of where the paraxial approximation is good for this element.
        """

        if self._curv != 0:
            return self._curv**-1 / 500
        else:
            return 1

    def _intercept(self, ray):
        """
        Calculates the first intercept of a ray with the surface described.
        """
        
        #vector difference between centre of curvature and ray position
        r = ray.pos() - self._center()
        l = None
    
        
        if self._curv != 0:
            #check if will intercept at all
            det = np.dot(r, ray.dirn())**2 - np.linalg.norm(r)**2 + (1/self._curv)**2
            if det < 0:
                return None
            
            #calculate the two intersections with the sphere
            a = -np.dot(r, ray.dirn())
            b = np.sqrt(det)
            
            #select based on curvature
            if self._curv < 0:
                l = a + b
            else:
                l = a - b
        else:
            #special case for a planar surface
            l = (self._z0 - ray.pos()[2]) / ray.dirn()[2]

        #check if intersection behind
        if l < 0:
            return None
        
        #check if point of intersection lies outside apt
        intercept = ray.pos() + l * ray.dirn()
        if not self._apt is None:
            if np.sqrt(intercept[0]**2 + intercept[1]**2) > self._apt:
                return None
        
        return intercept

class SphericalRefractor(SphericalElement):
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

        if callable(n1):
            self.__n1 = n1
        else:
            self.__n1 = lambda x : n1
        if callable(n2):
            self.__n2 = n2
        else:
            self.__n2 = lambda x : n2
        
        super().__init__(z0, curvature, apt)

        
    def __repr__(self):
        if not self._apt is None:
            return "elements.SphericalRefractor({:g}, {:g}, {}, {}, {:g})".format(self._z0, self._curv, self.__n1, self.__n2, self._apt)
        else:
            return "elements.SphericalRefractor({:g}, {:g}, {}, {})".format(self._z0, self._curv, self.__n1, self.__n2)

    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, or totally internally reflects, this method will return False, and won't update the ray.
        If the ray totally internally reflects, the ray will be terminated.
        """

        if ray.terminated():
            return False

        intercept = self._intercept(ray)
        
        if intercept is None:
            return False
        
        if (self._curv > 0 and ray.dirn()[2] > 0) or (self._curv < 0 and ray.dirn()[2] < 0):
            surface_normal = intercept - self._center()
        elif (self._curv < 0 and ray.dirn()[2] > 0) or (self._curv > 0 and ray.dirn()[2] < 0):
            surface_normal = self._center() - intercept
        else:
            surface_normal = np.array([0,0,-1.0 * ray.dirn()[2] / abs(ray.dirn()[2])])
            
        surface_normal /= np.linalg.norm(surface_normal)

        refracted_dirn = ou.refract(ray.dirn(), surface_normal, self.__n1(ray.wavelength()), self.__n2(ray.wavelength()))

        if not refracted_dirn is None:
            ray.append(intercept, refracted_dirn)
        else:
            ray.terminate()
            return False
        
class SphericalReflector(SphericalElement):
    """
    Represents a spherical reflecting surface.
    """

    def __init__(self, z0, curvature, apt=None, reverse_mirror=False):
        """
        z0: the intersection of the element with the z axis.
        curvature: 1/radius of curvature, this is negative if the centre of curvature is smaller than z0.
        apt: aperture radius.

        It is assumed that the side of the surface facing decreasing z is the reflecting one, if reverse_mirror is set to True, this will be flipped.
        """

        self.__reverse = reverse_mirror
        super().__init__(z0, curvature, apt)

    
    def __repr__(self):
        if not self._apt is None:
            return "elements.SphericalReflector({:g}, {:g}, {:g})".format(self._z0, self._curv, self._apt)
        else:
            return "elements.SphericalReflector({:g}, {:g})".format(self._z0, self._curv)
    
    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, or hits the non-reflective side, this method will return False, and won't update the ray.
        If the ray hits the non-reflective side, the ray will be terminated.
        """

        if ray.terminated():
            return False

        intercept = self._intercept(ray)
        
        if intercept is None:
            return False
            
        if (self._curv > 0 and ray.dirn()[2] > 0) or (self._curv < 0 and ray.dirn()[2] < 0):
            surface_normal = intercept - self._center()
        elif (self._curv < 0 and ray.dirn()[2] > 0) or (self._curv > 0 and ray.dirn()[2] < 0):
            surface_normal = self._center() - intercept
        else:
            surface_normal = np.array([0,0,-1.0 * ray.dirn()[2] / abs(ray.dirn()[2])])

        #terminate if hits non-reflective
        if (surface_normal[2] < 0 and self.__reverse) or (surface_normal[2] > 0 and not self.__reverse):
            ray.terminate()
            return False

        surface_normal /= np.linalg.norm(surface_normal)

        reflected_dirn = ou.reflect(ray.dirn(), surface_normal)

        if not reflected_dirn is None:
            ray.append(intercept, reflected_dirn)
        else:
            ray.terminate()
            return False
            
class OutputPlane(Element):
    """
    Represents a virtual plane that does not modify rays.
    """

    def __init__(self, z0):
        """
        z0: the intersection of the element with the z axis.
        """

        self._z0 = z0

    def __repr__(self):
        return "elements.OutputPlane({:g})".format(self._z0)
    

    def _intercept(self, ray):
        l = (self._z0 - ray.pos()[2]) / ray.dirn()[2]
        
        #check if behind
        if l < 0:
            return None
    
        intercept = ray.pos() + l * ray.dirn()
        
        return intercept
    
    def get_paraxial(self):
        """
        Gets a reasonable estimate for paraxial approximation: here returns 1, as OutputPlane does not modify the ray.
        """

        return 1

    def propagate(self, ray):
        """
        Propagates a ray through the element.
        If the ray does not intercept, this method will return False, and won't update the ray.
        """

        intercept = self._intercept(ray)
        
        if intercept is None:
            return False
        
        ray.append(intercept, ray.dirn().copy())
