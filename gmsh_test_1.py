import gmsh

# Initialization
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("My_Structure")

# Load STL Mesh
gmsh.merge('gmsh_test_1.stl')

#####################################################
# Entity Tag Identification (STL Handling)
# - STL does not have inherent groups so we find the surfaces based on their bounding box
surfaces = gmsh.model.getEntities(2)
print('\nNumber of surfaces: ' + str(len(surfaces)))
print('Surface tags:')
for s in surfaces:
    print(s)   

# create mesh surfaces using facet groups of 3
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
# Find surfaces that are on the ground and on the top
base_tol = 0.01
top_tol = 0.01

# Identify geometrical entities
TABLE_TOP = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmax - top_tol, xmax, ymax, zmax + top_tol, 2)
LEG_BOTTOMS = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmin - base_tol, xmax, ymax, zmin + base_tol, 2)

print(f'Top surfaces: {TABLE_TOP}\n')
print(f'Bottom surfaces: {LEG_BOTTOMS}\n')

surfaces = gmsh.model.getEntities(2)
print('Surfaces: ' + str(surfaces) + '\n')
print('Number of surfaces: ' + str(len(surfaces)) + '\n')

# Create a surface loop from the entire structure
surface_loop = gmsh.model.geo.addSurfaceLoop([s[1] for s in surfaces])
print('Surface Loop: ' + str(surface_loop) + '\n')

gmsh.model.geo.addVolume([surface_loop])
gmsh.model.geo.synchronize()
print('Volume: ' + str(gmsh.model.getEntities(3)) + '\n')

# Create a volume for the entire structure
#volume = gmsh.model.geo.addVolume([surface_loop])
#print('Volume: ' + str(volume) + '\n')

# Create fixed surfaces on the ground, and add a force on the top surfaces
gmsh.model.addPhysicalGroup(2, [e[1] for e in TABLE_TOP], -1)
gmsh.model.setPhysicalName(2, 1, "TABLE_TOP")
gmsh.model.addPhysicalGroup(2, [e[1] for e in LEG_BOTTOMS], -1)
gmsh.model.setPhysicalName(2, 2, "LEG_BOTTOMS")
gmsh.model.addPhysicalGroup(3, [e[1] for e in gmsh.model.getEntities(3)], -1)
gmsh.model.setPhysicalName(3, 1, "EALL")

'''
# Create a volume for the entire structure
gmsh.model.geo.synchronize()
volumes = gmsh.model.getEntities(3)
print('Volumes: ' + str(volumes) + '\n')

gmsh.model.addPhysicalGroup(3, [v[1] for v in volumes], 3)
gmsh.model.setPhysicalName(3, 3, "EALL")
'''

'''
nodes = gmsh.model.getEntities(0)
print('Nodes: ' + str(nodes) + '\n')

gmsh.model.addPhysicalGroup(0, [n[1] for n in nodes], 4)
gmsh.model.setPhysicalName(0, 4, "EALL")
'''

'''
for s in surfaces:
    # Get the bounding box of the surface
    sx_min, sy_min, sz_min, sx_max, sy_max, sz_max = gmsh.model.getBoundingBox(s[0], s[1])

    # Check if the surface is on the ground
    if sz_min < zmin + base_tol and sz_max < zmin + base_tol:
        ground_surfaces.append(s[1])
    # Check if the surface is on the top
    if sz_min > zmax - top_tol and sz_max > zmax - top_tol:
        top_surfaces.append(s[1])

print('Ground surfaces:')
print(ground_surfaces)
print('\n')
print('Top surfaces:')
print(top_surfaces)
'''

'''
ALL_ELEMENTS = gmsh.model.getEntities(3) # Get all elements
gmsh.model.addPhysicalGroup(3, [e[1] for e in ALL_ELEMENTS], 3)
gmsh.model.setPhysicalName(3, 3, "ALL_ELEMENTS")
for i in ALL_ELEMENTS:
    print(f"Element {i[1]}")
'''

#####################################################
# Meshing parameters
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.2)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.5)

# Create mesh
gmsh.model.mesh.generate(3)

# Write mesh to file
gmsh.write("gmsh_test_1.msh")

# Visualize the mesh
gmsh.fltk.run()
gmsh.finalize()