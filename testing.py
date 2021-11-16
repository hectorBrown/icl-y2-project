# -*- coding: utf-8 -*-
"""
Testing module.
"""

import matplotlib.pyplot as plt, numpy as np
import elements as e, graphics as g, opticsutils as ou, ray as r

def t9():
    refractor = e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5)
    output = e.OutputPlane(250e-3)
    bundle = r.bundle(5e-3, 6, 6)
    
    for ray in bundle:
        refractor.propagate(ray)
        output.propagate(ray)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 250e-3))

def t10():
    refractor = e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5)
    output = e.OutputPlane(250e-3)
    bundle = [r.Ray([0,0,0], [0,0,1]), r.Ray([0,0.1e-3,0], [0,0,1])]
    
    for ray in bundle:
        refractor.propagate(ray)
        output.propagate(ray)
    
    return g.graph_yplane(bundle)

def t11():
    refractor = e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5)
    output = e.OutputPlane(400e-3)
    bundle = [r.Ray([0, 2e-3, 0], [0,0,1]),
              r.Ray([0, 2e-3, 0], [0, -2e-3, 100e-3]),
              r.Ray([0, 2e-3, 0], [0, -4e-3, 100e-3])]
    
    for ray in bundle:
        refractor.propagate(ray)
        output.propagate(ray)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 400e-3))

def t12():
    refractor = e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5)
    output = e.OutputPlane(250e-3)
    bundle = r.bundle(5e-3, 8, 6)
    
    for ray in bundle:
        refractor.propagate(ray)
        output.propagate(ray)
    
    #focal length = nR/(n-1)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 200e-3))

def t13():
    refractor = e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5)
    output = e.OutputPlane(250e-3)
    bundle = r.bundle(5e-3, 6, 6)
    
    for ray in bundle:
        refractor.propagate(ray)
        output.propagate(ray)
        
    spots = [np.linalg.norm(r.get_xy(200e-3))**2 for r in bundle]
    
    return np.sqrt(np.average(spots))

def t15():
    lens_1 = [e.SphericalRefractor(100e-3, 0, 1, 1.5168),
            e.SphericalRefractor(105e-3, -0.02e3, 1.5168, 1)]
    lens_2 = [e.SphericalRefractor(100e-3, 0.02e3, 1, 1.5168),
              e.SphericalRefractor(105e-3, 0, 1.5168, 1)]
    
    focus_1, focus_2 = ou.get_focus(lens_1), ou.get_focus(lens_2)
    spot_size_1 = [ou.spot_size(lens_1, focus=focus_1, bundle_radius=x * 1e-3) for x in range(1,11)]
    spot_size_2 = [ou.spot_size(lens_2, focus=focus_2, bundle_radius=x * 1e-3) for x in range(1,11)]
    
    return {"correct": (focus_2, spot_size_2), "reverse": (focus_1, spot_size_1)}
    

