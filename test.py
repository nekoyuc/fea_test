import os
import json
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi
import pygame
import pyvista as pv

#file = "1452670.stl"
file = "1147240.stl"
inpath = "Thingi10K/debug/"
outpath = "Thingi10K/debug/"
mp(file, inpath, outpath)
#mi(outpath + file.replace(".stl", ".inp"))

'''
# Load the mesh file
mesh = pv.read("Thingi10K/viz_experiment/500099.msh")

# Create a plotter
plotter = pv.Plotter()

# Add the mesh to the plotter
plotter.add_mesh(mesh)

#table_top = mesh.extract_cells_by_type("GROUP_ID", "TABLE_TOP")

# Display the plotter
plotter.show()
'''