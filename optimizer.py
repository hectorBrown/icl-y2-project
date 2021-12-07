# -*- coding: utf-8 -*-
"""
A module for singlet lens optimization.
"""

import scipy.optimize as op
import elements as e, opticsutils as ou

def __spot_size_optimizer(c1, focus, z1, z2, n1, n2):
    """
    Utility method for optimizing spot size.
    """

    lens = e.System(elements=[e.SphericalRefractor(z1, c1, n1, n2),
            e.SphericalRefractor(z2, ou.get_c2(c1, focus), n2, n1)])
    return ou.spot_size(lens)

def optimize(focus, z1, z2, n1, n2, c1_0=0):
    """
    Find optimal curvature for a given lens setup.
    c1_0: optional initial guess for ideal c1 (may help optimization converge).
    Returns a tuple of (c1, c2) where c_n is the curvature of the nth surface.
    """

    c1 = op.minimize(lambda x : __spot_size_optimizer(x, focus, z1, z2, n1, n2), c1_0, method="Nelder-Mead")["x"][0]
    return (c1, ou.get_c2(c1, focus))
