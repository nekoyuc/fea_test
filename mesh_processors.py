import gmsh
import json
import math

#with open('config.json') as f:
#    config = json.load(f)

def mesh_processing(file_name, file_path, output_path):
    # Initialization
    gmsh.initialize(interruptible = False)
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("My_Structure")
    gmsh.merge(file_path + file_name)

    #####################################################
    # create mesh surfaces using facet groups of 3
    #gmsh.model.mesh.createTopology()
    gmsh.model.mesh.classifySurfaces(1e-6)
    print('Classified Surfaces\n')
    gmsh.model.mesh.createGeometry()
    print('Created Geometry')
    # Determine bounding box
    xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)

    #####################################################
    surfaces = gmsh.model.getEntities(2)
    print('Surfaces: ' + str(surfaces) + '\n')

    # Create a surface loop from the entire structure
    surface_loop = gmsh.model.geo.addSurfaceLoop([s[1] for s in surfaces])
    print('Surface Loop: ' + str(surface_loop) + '\n')

    gmsh.model.geo.addVolume([surface_loop])
    gmsh.model.geo.synchronize()

    # Create fixed surfaces on the ground, and add a force on the top surfaces
    base_tol = 0.01
    top_tol = 0.01
    TABLE_TOP = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmax - top_tol, xmax, ymax, zmax + top_tol, 0)
    LEG_BOTTOMS = gmsh.model.getEntitiesInBoundingBox(xmin, ymin, zmin - base_tol, xmax, ymax, zmin + base_tol, 0)

    gmsh.model.addPhysicalGroup(0, [n[1] for n in gmsh.model.getEntities(0)], 1001, "NODES")
    gmsh.model.addPhysicalGroup(0, [e[1] for e in TABLE_TOP], 2001, "TABLE_TOP")
    gmsh.model.addPhysicalGroup(0, [e[1] for e in LEG_BOTTOMS], 2002, "LEG_BOTTOMS")
    gmsh.model.addPhysicalGroup(3, [e[1] for e in gmsh.model.getEntities(3)], 3001, "VOLUME")

    #####################################################
    # Meshing parameters
    gmsh.option.setNumber("Mesh.Algorithm", 6)  # Set algorithm to generate hexahedron mesh
    gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Set algorithm for 3D meshing to Delaunay
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 10)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 50)
    #gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 2)
    gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", 0.00001)
    print('Meshing Parameters Set\n')
    # Create 20-node hexahedrons
    #gmsh.option.setNumber("Mesh.ElementOrder", 2)
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
    #gmsh.write(file_path.split("/")[-1].replace(".stl", "") + ".inp")
    inp_file = output_path + file_name
    inp_file = inp_file.replace(".stl", ".inp")
    gmsh.write(inp_file)

    # Write mesh to file
    #gmsh.write(output_path + file_name.replace(".stl", ".msh"))

    # Visualize the mesh
    #gmsh.fltk.run()
    gmsh.finalize()
    
    # Export mesh to obj
    #gmsh.write("file.obj")

    return inp_file

def modify_inp(inp_file_path):
    #file_path = file_path.replace(".stl", ".inp")
    # Open the file in append mode
    #file_path = "gmsh_test_12.inp"
    with open(inp_file_path, "a") as file:
        # Add additional contents at the end of the file
        additional_contents = "\n*MATERIAL, NAME=TableMaterial\n"
        additional_contents += "*ELASTIC, TYPE=ISO\n"
        additional_contents += "30000, 0.3\n\n"

        additional_contents += "*SOLID SECTION,MATERIAL=TableMaterial,ELSET=VOLUME\n\n"

        additional_contents += "*BOUNDARY, FIXED\n"
        additional_contents += "LEG_BOTTOMS,1,3\n\n"

        additional_contents += "*STEP,INC=100,NLGEOM=YES\n"
        additional_contents += "*STATIC\n\n"

        additional_contents += "*DLOAD\n"
        additional_contents += "VOLUME, P1, -10\n\n"
    
        additional_contents += "*NODE FILE,GLOBAL=YES, NSET=VOLUME\n"
        additional_contents += "RF,U\n\n"

    
        additional_contents += "*EL FILE,GLOBAL=YES, VOLUME\n"
        additional_contents += "ME,S\n\n"
    
        additional_contents += "*END STEP\n"

        file.write(additional_contents)
    
def check_water_tightness(ms):
    measures = ms.apply_filter("get_geometric_measures")
    # Check if key "inertia_tensor" exists in the measures dictionary. If so, mesh is watertight.
    if "inertia_tensor" in measures:
        # Key "inertia_tensor" exists in the measures dictionary
        print("Mesh is watertight")
        return True
    else:
        # Key "inertia_tensor" does not exist in the measures dictionary
        print("Mesh is not watertight")
        return False