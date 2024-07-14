import json

# Load the configuration file
#with open('config.json') as f:
#    config = json.load(f)

#file_path = config['file_path'].split("/")[-1].replace(".stl", "") + ".inp"

def modify_inp(inp_file):
    #file_path = file_path.replace(".stl", ".inp")
    # Open the file in append mode
    #file_path = "gmsh_test_12.inp"
    with open(inp_file, "a") as file:
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

# The file will be automatically saved and closed when the 'with' block ends
