# -*- coding: utf-8 -*-
"""
Contains the Element base class, and all derived classes.
"""
class Element:
    def propagate(self, ray):
        """
        Propagate a ray through the optical element.
        """
        raise NotImplementedError()
