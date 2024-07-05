import netgen.stl
import netgen.gui
from netgen.geom2d import unit_square
from netgen.csg import *
import netgen.meshing as ngm
import ngsolve
from ngsolve.webgui import Draw
import ngsolve.webgui

# load a mesh from a stl file
stl_geo = netgen.stl.STLGeometry("gmsh_test_1.stl")
mesh = stl_geo.GenerateMesh(maxh=0.5)

# draw the mesh
ngsolve.webgui.Draw(mesh)

mesh.Export("gmsh_test_1.vol")