# -*- coding: utf-8 -*-
"""
Testing module.
"""

import numpy as np, matplotlib.pyplot as plt
import elements as e, graphics as g, opticsutils as ou, ray as r, optimizer as ot

def t9():
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5))
    sys.append(e.OutputPlane(250e-3))
    bundle = [r.Ray([0, (x / 10) * 1e-3, 0], [0,0,1]) for x in range(25)]
    
    sys.propagate(bundle)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 250e-3))

def t10():
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5))
    sys.append(e.OutputPlane(250e-3))
    bundle = [r.Ray([0,0,0], [0,0,1]), r.Ray([0,0.1e-3,0], [0,0,1])]
    
    sys.propagate(bundle)
    
    return g.graph_yplane(bundle)

def t11():
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5))
    sys.append(e.OutputPlane(400e-3))
    bundle = [r.Ray([0, 2e-3, 0], [0,0,1]),
              r.Ray([0, 2e-3, 0], [0, -2e-3, 100e-3]),
              r.Ray([0, 2e-3, 0], [0, -4e-3, 100e-3])]
    
    sys.propagate(bundle)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 400e-3))

def t12():
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5))
    sys.append(e.OutputPlane(250e-3))
    bundle = r.bundle(5e-3, 6, 6)
    
    sys.propagate(bundle)
    
    #focal length = nR/(n-1)
    
    return (g.graph_yplane(bundle), g.graph_zplane(bundle, 250e-3))

def t13():
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.03e3, 1, 1.5))
    sys.append(e.OutputPlane(250e-3))
    bundle = r.bundle(5e-3, 6, 6)
    
    sys.propagate(bundle)
        
    spots = [np.linalg.norm(r.get_xy(200e-3))**2 for r in bundle]
    
    return (np.sqrt(np.average(spots)), g.graph_zplane(bundle, 200e-3))

def t15():
    lens_1 = e.System(elements=[e.SphericalRefractor(100e-3, 0, 1, 1.5168),
            e.SphericalRefractor(105e-3, -0.02e3, 1.5168, 1)])
    lens_2 = e.System(elements=[e.SphericalRefractor(100e-3, 0.02e3, 1, 1.5168),
              e.SphericalRefractor(105e-3, 0, 1.5168, 1)])
    
    focus_1, focus_2 = ou.get_focus(lens_1), ou.get_focus(lens_2)
    spot_size_1 = [ou.spot_size(lens_1, focus=focus_1, bundle_radius=x * 1e-3) for x in range(1,11)]
    spot_size_2 = [ou.spot_size(lens_2, focus=focus_2, bundle_radius=x * 1e-3) for x in range(1,11)]
    
    bundle_1, bundle_2 = r.bundle(15e-3, 6, 6), r.bundle(15e-3, 6, 6)
    sys_1 = lens_1.copy(); sys_1.append(e.OutputPlane(250e-3))
    sys_2 = lens_2.copy(); sys_2.append(e.OutputPlane(250e-3))
    sys_1.propagate(bundle_1); sys_2.propagate(bundle_2)
    
    
    return ({"correct": (focus_2, spot_size_2), "reverse": (focus_1, spot_size_1)},
             g.graph_yplane(bundle_1), g.graph_yplane(bundle_2))
    
def optimization_ext():
    lens_setup = [t15()[0]["correct"][0], 100e-3, 105e-3, 1, 1.5168]
    fig_curv = g.graph_spot_size((0, 30), 0.5, *lens_setup)

    curvs = ot.optimize(*lens_setup)
    return (fig_curv, curvs)

def chromatic_ext():
    def index_func(wavelength):
        return 1.5168 + (wavelength - 380e-9) / (740e-9 - 380e-9) * 0.001
    sys = e.System()
    sys.append(e.SphericalRefractor(100e-3, 0.02e3, 1, index_func))
    sys.append(e.SphericalRefractor(105e-3, 0, index_func, 1))
    sys.append(e.OutputPlane(250e-3))
    red = r.bundle(10e-3, 6, 6, wavelength=380e-9)
    green = r.bundle(10e-3, 6, 6, wavelength=(740 + 380) / 2 * 1e-9)
    blue = r.bundle(10e-3, 6, 6, wavelength=740e-9)
    bundle = np.array(list(red) + list(green) + list(blue))
    
    sys.propagate(bundle)

    return g.graph_zplane(bundle, 200e-3)

def reflecting_ext():
    sys = e.System()
    sys.append(e.SphericalReflector(100e-3, -0.02e3))
    sys.append(e.OutputPlane(-50e-3))
    bundle = r.bundle(10e-3, 6, 6)

    sys.propagate(bundle)

    return g.graph_yplane(bundle)

def rainbow():
    sys = e.System()
    water_index = ou.load_index("data/water.csv")
    sys.append(e.SphericalRefractor(10e-3, (1e-3)**-1, 1, lambda l : ou.get_index(water_index, l)))
    sys.append(e.SphericalReflector(12e-3, -(1e-3)**-1))
    sys.append(e.SphericalRefractor(10e-3, (1e-3)**-1, lambda l : ou.get_index(water_index, l), 1))
    sys.append(e.OutputPlane(0.0))
      
    bundle = [r.Ray([0, 0.9e-3, 0], [0, 0, 20e-3], wavelength=(380e-9 + (i/10) * (740e-9 - 380e-9))) for i in range(11)]

    
    sys.propagate(bundle)
    
    return g.graph_yplane(bundle)

def get_required_plots():
    fig = t9()[0]
    plt.figure(fig.number)
    plt.title("Example rays in a single spherical refracting surface")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("z-coordinate (m)")
    plt.tight_layout()
    plt.savefig("t9.png", dpi=200)
    
    fig = t11()[0]
    plt.figure(fig.number)
    plt.title("Example rays in a single spherical refracting surface")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("z-coordinate (m)")
    plt.tight_layout()
    plt.savefig("t11.png", dpi=200)
    
    figs = t12()
    fig = figs[0]
    plt.figure(fig.number)
    plt.title("Collimated ray bundle in a single spherical refracting surface")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("z-coordinate (m)")
    plt.tight_layout()
    plt.savefig("t12_1.png", dpi=200)
    
    fig = figs[1]
    plt.figure(fig.number)
    plt.title("Collimated ray bundle in a single spherical refracting surface\n(z=250mm)")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("x-coordinate (m)")
    plt.ticklabel_format(style="sci", scilimits=(0,0))
    plt.tight_layout()
    plt.savefig("t12_2.png", dpi=200)
    
    fig = t13()[1]
    plt.figure(fig.number)
    plt.title("Spot size diagram at paraxial focus of spherical refracting surface\n(z=200mm)")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("x-coordinate (m)")
    plt.ticklabel_format(style="sci", scilimits=(0,0))
    plt.tight_layout()
    plt.savefig("t13.png", dpi=200)
    
    data, *figs = t15()
    fig = figs[0]
    plt.figure(fig.number)
    plt.title("Incorrect orientation singlet lens")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("z-coordinate (m)")
    plt.tight_layout()
    plt.savefig("t15_1.png", dpi=200)
    
    fig = figs[1]
    plt.figure(fig.number)
    plt.title("Correct orientation singlet lens")
    plt.ylabel("y-coordinate (m)")
    plt.xlabel("x-coordinate (m)")
    plt.tight_layout()
    plt.savefig("t15_2.png", dpi=200)
    
    fig = plt.figure()
    plt.title("Singlet lens orientation and performance")
    plt.xlabel("Bundle size (m)")
    plt.ylabel("RMS spot size (m)")
    plt.plot(np.array(range(1,11)) * 1e-3, data["correct"][1], label="Correct orientation")
    plt.plot(np.array(range(1,11)) * 1e-3, data["reverse"][1], label="Reverse orientation")
    plt.legend()
    plt.savefig("t15_3.png", dpi=200)
    
    fig, data = optimization_ext()
    plt.figure(fig.number)
    plt.title("Fixed-focus RMS spot-size against curvature")
    plt.xlabel("Curvature of first lens (m^-1)")
    plt.ylabel("RMS spot size (m)")
    plt.tight_layout()
    plt.savefig("opt_1.png", dpi=200)
    
    bundle = r.bundle(10e-3, 6, 6)
    sys = e.System([e.SphericalRefractor(100e-3, data[0], 1, 1.5168),
                    e.SphericalRefractor(105e-3, data[1], 1.5168, 1),
                    e.OutputPlane(250e-3)])
    sys.propagate(bundle)
    #system elements are non-accessible
    fig = g.graph_zplane(bundle, ou.get_focus(sys.elements()[:-1]))
    plt.title("Optimized focal plane spot size")
    plt.xlabel("x-coordinate (m)")
    plt.ylabel("y-coordinate (m)")
    plt.savefig("opt_2.png", dpi=200)
