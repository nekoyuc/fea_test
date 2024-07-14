import gmsh
import json
import math


with open('config.json') as f:
    config = json.load(f)


# Initialization
gmsh.initialize(interruptible = False)
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("My_Structure")

# Load STL Mesh
file_path = config['file_path']
#file_path = 'Thingi10K/raw_meshes/36069.stl'
#file_path = 'gmsh_test_1.stl'
gmsh.merge(file_path)

#####################################################
# create mesh surfaces using facet groups of 3
gmsh.model.mesh.createTopology()
gmsh.model.mesh.classifySurfaces(1e-6)
print('Classified Surfaces\n')
gmsh.model.mesh.createGeometry()
print('Created Geometry')

# Determine bounding box
xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)
print('Bounding Box:')
print('xmin: ' + str(xmin))
print('ymin: ' + str(ymin))
print('zmin: ' + str(zmin))
print('xmax: ' + str(xmax))
print('ymax: ' + str(ymax))
print('zmax: ' + str(zmax))

#####################################################
surfaces = gmsh.model.getEntities(2)

# Create a surface loop from the entire structure
surface_loop = gmsh.model.geo.addSurfaceLoop([s[1] for s in surfaces])
print('Surface Loop: ' + str(surface_loop) + '\n')

gmsh.model.geo.addVolume([surface_loop])
gmsh.model.geo.synchronize()

'''
# Retag entities
for i, p in enumerate(gmsh.model.getEntities(0)):
    gmsh.model.setTag(0, p[1], 1001 + i)

for i, l in enumerate(gmsh.model.getEntities(1)):
    gmsh.model.setTag(1, l[1], 1101 + i)

for i, s in enumerate(gmsh.model.getEntities(2)):
    gmsh.model.setTag(2, s[1], 1201 + i)

for i, v in enumerate(gmsh.model.getEntities(3)):
    gmsh.model.setTag(3, v[1], 1301 + i)
'''

# Create fixed surfaces on the ground, and add a force on the top surfaces
# add a node set of all nodes
# Find surfaces that are on the ground and on the top
base_tol = 0.01
top_tol = 0.01
TABLE_TOP = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmax - top_tol, xmax, ymax, zmax + top_tol, 0)
LEG_BOTTOMS = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmin - base_tol, xmax, ymax, zmin + base_tol, 0)

gmsh.model.addPhysicalGroup(0, [n[1] for n in gmsh.model.getEntities(0)], 2001, "NODES")
gmsh.model.addPhysicalGroup(0, [e[1] for e in TABLE_TOP], 2201, "TABLE_TOP")
gmsh.model.addPhysicalGroup(0, [e[1] for e in LEG_BOTTOMS], 2202, "LEG_BOTTOMS")
gmsh.model.addPhysicalGroup(3, [e[1] for e in gmsh.model.getEntities(3)], 2301, "VOLUME")

#####################################################
# Meshing parameters
gmsh.option.setNumber("Mesh.Algorithm", 6)  # Set algorithm to generate hexahedron mesh
gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Set algorithm for 3D meshing to Delaunay
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 10)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 10000000)
#gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 2)
gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", 0.00001)
print('Meshing Parameters Set\n')
# Create 20-node hexahedrons
gmsh.option.setNumber("Mesh.ElementOrder", 1)
#gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

# Create mesh
gmsh.model.mesh.generate(3)
#gmsh.model.mesh.refine()

points = gmsh.model.getEntities(0)
lines = gmsh.model.getEntities(1)
surfaces = gmsh.model.getEntities(2)
volumes = gmsh.model.getEntities(3)
print(f'Top surfaces: {TABLE_TOP}\n')
print(f'Bottom surfaces: {LEG_BOTTOMS}\n')
#print('Points: ' + str(points))
print('Number of points: ' + str(len(points)) + '\n')
#print('Lines: ' + str(lines))
print('Number of lines: ' + str(len(lines)) + '\n')
#print('Surfaces: ' + str(surfaces))
print('Number of surfaces: ' + str(len(surfaces)) + '\n')
#print('Volumes: ' + str(volumes))
print('Number of volumes: ' + str(len(volumes)) + '\n')

#gmsh.option.setNumber("Mesh.SaveAll", 1)
#gmsh.option.setNumber("Mesh.SaveGroupsOfElements", 1)
gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)

# Export to inp file
gmsh.write(file_path.split("/")[-1].replace(".stl", "") + ".inp")

# Write mesh to file
#gmsh.write("gmsh_test_1.msh")

# Visualize the mesh
gmsh.fltk.run()
gmsh.finalize()