import os
import json
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi
import pygame
import pyvista as pv
import subprocess

#file = "1452670.stl"
file = "1147240.stl"
inpath = "Thingi10K/debug/"
outpath = "Thingi10K/raw_meshes/Batch14_results/"
#mp(file, inpath, outpath)
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

list = os.listdir(outpath)
print("length of list: " + str(len(list)))
files = []

# delete files that do not end with ".stl"
for i in list:
    # get the last 4 characters of the file name
    file_extension = i[-4:]
    if file_extension == ".frd":
        print(f"To add: {i}")
        files.append(i)

print("length of files: " + str(len(files)))

for file in files:
    command = "cgx " + outpath + file
    subprocess.run(f"{command} | tail -n 6", shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)