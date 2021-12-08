from testing import *

fig = t9()[0]
plt.figure(fig.number)
plt.title("Example rays in a single spherical refracting surface")
plt.ylabel("y-coordinate (m)")
plt.xlabel("z-coordinate (m)")
plt.tight_layout()
plt.savefig("t9.png", dpi=200)

fig = t11()[0]
plt.figure(fig.number)
plt.title("Principle rays forming an image in spherical refracting surface")
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
plt.tight_layout()
plt.savefig("t15_3.png", dpi=200)

fig, data = optimization_ext()
plt.figure(fig.number)
plt.title("Fixed-focus RMS spot-size against curvature")
plt.xlabel("Curvature of first lens (m^-1)")
plt.ylabel("RMS spot size (m)")
plt.tight_layout()
plt.savefig("opt_1.png", dpi=200)

bundle = r.bundle(10e-3, 6, 6)
lens = e.System([e.SphericalRefractor(100e-3, data[0], 1, 1.5168),
                e.SphericalRefractor(105e-3, data[1], 1.5168, 1)])
                
sys = lens.copy(); sys.append(e.OutputPlane(250e-3))
sys.propagate(bundle)
#system elements are non-accessible
fig = g.graph_zplane(bundle, ou.get_focus(lens))
plt.title("Optimized focal plane spot size")
plt.xlabel("x-coordinate (m)")
plt.ylabel("y-coordinate (m)")
plt.savefig("opt_2.png", dpi=200)

fig = chromatic_ext()
plt.figure(fig.number)
plt.title("Singlet lens model with chromatic abberation")
plt.xlabel("x-coordinate (m)")
plt.ylabel("y-coordinate (m)")
plt.tight_layout()
plt.savefig("chr.png", dpi=200)

fig = reflecting_ext()
plt.figure(fig.number)
plt.title("Example of a reflector")
plt.xlabel("z-coordinate (m)")
plt.ylabel("y-coordinate (m)")
plt.tight_layout()
plt.savefig("ref.png", dpi=200)

fig = rainbow()
plt.figure(fig.number)
plt.title("Demonstration of rainbow formation")
plt.xlabel("z-coordinate (m)")
plt.ylabel("y-coordinate (m)")
plt.tight_layout()
plt.savefig("rai.png", dpi=200)
