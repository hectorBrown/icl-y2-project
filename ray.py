# -*- coding: utf-8 -*-
"""
Contains the ray class.
"""

import numpy as np

class Ray:
    """
    Describes an optical ray with a trail of positions and directions.
    """
    
    def __init__(self, init_pt, init_dir):
        self.__pts = [init_pt]
        self.__dirs = [init_dir / np.linalg.norm(init_dir)]
    
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
    

