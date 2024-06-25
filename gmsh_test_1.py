import gmsh

# Initialization
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("My_Structure")

# Load STL Mesh
gmsh.merge('test.stl')

# Entity Tag Identification (STL Handling)
# - STL does not have inherent groups so we find the surfaces based on their bounding box
surfaces = gmsh.model.getEntities(2)
print('Number of surfaces: ' + str(len(surfaces)))
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

# Identify base and top surfaces based on z-coordinates (adjust tolerances if needed)
base_tol = 0.01
top_tol = 0.01
base_surfaces = []
top_surfaces = []

'''
base_surface_tag = 1 
top_surface_tag = 2
'''