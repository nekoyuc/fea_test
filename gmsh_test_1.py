import gmsh

# Initialization
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("My_Structure")

# Load STL Mesh
gmsh.merge('gmsh_test_1.stl')

# Entity Tag Identification (STL Handling)
# - STL does not have inherent groups so we find the surfaces based on their bounding box
surfaces = gmsh.model.getEntities(2)
print('Entities: ' + str(surfaces) + '\n')
# create mesh surfaces using facet groups of 3
gmsh.model.mesh.classifySurfaces(1e-6)
print('Classified Surfaces\n')
gmsh.model.mesh.createGeometry()
print('Created Geometry')

# Get the number of surfaces and their tags
surfaces = gmsh.model.getEntities(2)
print('\nNumber of surfaces: ' + str(len(surfaces)))
print('Surface tags:')
for s in surfaces:
    print(s)

# Determine bounding box
xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)

print('Bounding Box:')
print('xmin: ' + str(xmin))
print('ymin: ' + str(ymin))
print('zmin: ' + str(zmin))
print('xmax: ' + str(xmax))
print('ymax: ' + str(ymax))
print('zmax: ' + str(zmax))

# Find surfaces that are on the ground and on the top
#ground_surfaces = []
#top_surfaces = []
base_tol = 0.01
top_tol = 0.01

# Identify geometrical entities
table_top = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmax - top_tol, xmax, ymax, zmax + top_tol, 2)
leg_bottoms = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmin - base_tol, xmax, ymax, zmin + base_tol, 2)

print(f'Top surfaces: {table_top}\n')
print(f'Bottom surfaces: {leg_bottoms}\n')

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

# Create fixed surfaces on the ground, and add a force on the top surfaces
gmsh.model.addPhysicalGroup(2, [e[1] for e in table_top], 1)
gmsh.model.setPhysicalName(2, 1, "FixedSurfaces")
gmsh.model.addPhysicalGroup(2, [e[1] for e in leg_bottoms], 2)
gmsh.model.setPhysicalName(2, 2, "ForceSurfaces")

# Meshing parameters
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.02)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)

# Create mesh
gmsh.model.mesh.generate(3)

# Write mesh to file
gmsh.write("gmsh_test_1.msh")

# Visualize the mesh
gmsh.fltk.run()
gmsh.finalize()