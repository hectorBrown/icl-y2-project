# -*- coding: utf-8 -*-
"""
A module for singlet lens optimization.
"""

import elements as e, opticsutils as ou

def spot_size_optimizer(c1, focus, z1=100e-3, z2=105e-3, n1=1, n2=1.5168):
    lens = [e.SphericalRefractor(z1, c1, n1, n2),
            e.SphericalRefractor(z2, ou.get_c2(c1, focus), n2, n1)]
    return ou.spot_size(lens)
