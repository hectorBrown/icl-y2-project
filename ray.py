# -*- coding: utf-8 -*-
"""
Contains the ray class.
"""

import numpy as np, copy

def bundle(r, n_rings, n_rays):
    """
    Generates a bundle of rays of radius r.
    n_rings is the number of concentric rings to build the bundle of (incuding the central ray).
    n_rays is the number of rays to be equally spaced about the first ring.
    """

    rays = []

    #walk outwards through rings
    r_step = r / n_rings
    for i in range(n_rings + 1):
        if i == 0:
            #if central ray
            rays.append(Ray(np.array([0, 0, 0]), np.array([0, 0, 1])))
        else:
            #walk around circle
            the_step = 2 * np.pi / (n_rays * i)
            for j in range(n_rays * i):
                #calculated final values
                r_n = r_step * i
                the_n = the_step * j
                rays.append(Ray(np.array([r_n * np.cos(the_n), r_n * np.sin(the_n), 0]), np.array([0, 0, 1])))
    return rays

class Ray:
    """
    Describes an optical ray with a trail of positions and directions.
    """
    
    def __init__(self, init_pt, init_dir):
        self.__pts = [init_pt]
        if np.linalg.norm(init_dir) != 0:
            #normalise direction (essentially for easy testing)
            self.__dirs = [init_dir / np.linalg.norm(init_dir)]
        else:
            raise Exception("Ray can not have no direction.")
    
    def __repr__(self):
        return "ray.Ray {{pts: {}, dirs: {}}}".format(self.__pts, self.__dirs)
        
    def pos(self):
        """
        Returns the current (most recently added) point in the trail.
        """

        return self.__pts[-1]
    
    def dirn(self):
        """
        Returns the current (most recently added) direction in the trail.
        """

        return self.__dirs[-1]
    
    def append(self, next_pt, next_dir):
        """
        Appends a new point-direction pair to the trail.
        """

        self.__pts.append(next_pt)
        #again normalise direction
        self.__dirs.append(next_dir / np.linalg.norm(next_dir))
    
    def vertices(self):
        """
        Returns the full trail (no directions).
        """

        return self.__pts
    
    def copy(self):
        r = Ray(np.array([0,0,0]), np.array([0,0,1]))
        r.__pts = copy.deepcopy(self.__pts)
        r.__dirs = copy.deepcopy(self.__dirs)
        return r
    
    def get_xy(self, z):
        """
        Returns the x,y values for a given z, returns None if the ray does not exist at that z.
        If the ray is multi-valued at this z, returns the chronologically earlier point.
        """

        #check if any point as at the z value anyway
        if all([x[2] != z for x in self.__pts]):
            #produce a series of pairs of points
            for i in range(len(self.__pts) - 1):
                pair = (self.__pts[i], self.__pts[i + 1])
                #if z lies between these points
                if (z >= pair[0][2] and z <= pair[1][2]) or (z <= pair[0][2] and z >= pair[1][2]):
                    dirn = pair[1] - pair[0]
                    t = (z - pair[0][2])/dirn[2]
                    pt = pair[0] + t * dirn
                    return pt[:-1]
            return None
        else:
            for pt in self.__pts:
                if pt[2] == z:
                    return pt[:-1]