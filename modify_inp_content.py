# Open the file in append mode
file_path = "gmsh_test_12.inp"
with open(file_path, "a") as file:
    # Add additional contents at the end of the file
    additional_contents = "\n*MATERIAL, NAME=TableMaterial\n"
    additional_contents += "*ELASTIC, TYPE=ISO\n"
    additional_contents += "30000, 0.3\n\n"

    additional_contents += "*SOLID SECTION,MATERIAL=TableMaterial,ELSET=VOLUME\n\n"

    additional_contents += "*BOUNDARY, FIXED\n"
    additional_contents += "LEG_BOTTOMS,1,3\n\n"

    additional_contents += "*STEP,INC=1000,NLGEOM=YES\n"
    additional_contents += "*STATIC\n\n"

    additional_contents += "*DLOAD\n"
    additional_contents += "VOLUME, P1, -100\n\n"
    
    additional_contents += "*NODE FILE,GLOBAL=YES, NSET=VOLUME\n"
    additional_contents += "RF,U\n\n"
    
    
    additional_contents += "*EL FILE,GLOBAL=YES, VOLUME\n"
    additional_contents += "ME,S\n\n"
    
    additional_contents += "*END STEP\n"

    file.write(additional_contents)

# The file will be automatically saved and closed when the 'with' block ends

'''
** Material Properties (Replace 'a' with the actual Young's modulus value)
*MATERIAL,NAME=TableMaterial
*ELASTIC, TYPE = ISO
30000, 0.3

** Element Set
*ELSET,ELSET=EALL,GENERATE
0,0

*NSET,NSET=NALL,GENERATE
0,0

** Section
*SOLID SECTION,MATERIAL=TableMaterial,ELSET=EALL

** Boundary Conditions
*BOUNDARY LEG_BOTTOMS, 1, 3  # Fix all displacements for leg bottoms

** Load
*DLOAD TABLE_TOP, P, -100  # Uniform downward pressure (adjust -100 as needed)

** Step
*STEP
*STATIC

** Output Request
*NODE FILE,GLOBAL=YES,NSET=NALL
U
*EL FILE,ELSET=EALL
S,MISES

** End Step
*END STEP
'''