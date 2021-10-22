# -*- coding: utf-8 -*-
"""
Contains the ray class.
"""


class Ray:
    """
    Describes an optical ray with a trail of positions and directions.
    """
    
    def __init__(self, init_pt, init_dir):
        self.__pts = [init_pt]
        self.__dirs = [init_dir]
    
    def curr_pt(self):
        """
        Returns the current (most recently added) point in the trail.
        """
        return self.__pts[-1]
    
    def curr_dir(self):
        """
        Returns the current (most recently added) direction in the trail.
        """
        return self.__dirs[-1]
    
    def append(self, next_pt, next_dir):
        """
        Appends a new point-direction pair to the trail.
        """
        self.__pts.append(next_pt)
        self.__dirs.append(next_dir)
    
    def vertices(self):
        """
        Returns the full trail (no directions).
        """
        return self.__pts
    

