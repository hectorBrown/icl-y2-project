# -*- coding: utf-8 -*-
"""
Contains the ray class.
"""

import numpy as np
import copy

class Ray:
    """
    Describes an optical ray with a trail of positions and directions.
    """
    
    def __init__(self, init_pt, init_dir):
        self.__pts = [init_pt]
        if np.linalg.norm(init_dir) != 0:
            self.__dirs = [init_dir / np.linalg.norm(init_dir)]
        else:
            raise Exception("Ray can not have no direction.")
        
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
