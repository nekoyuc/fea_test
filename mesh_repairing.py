import pymeshlab

file_path = "Thingi10K/selected/36075.stl"
ms = pymeshlab.MeshSet()
ms.load_new_mesh(file_path)

def check_water_tightness(ms):
    measures = ms.apply_filter("get_geometric_measures")
    # Check if key "inertia_tensor" exists in the measures dictionary. If so, mesh is watertight.
    if "inertia_tensor" in measures:
        # Key "inertia_tensor" exists in the measures dictionary
        print(measures["inertia_tensor"])
        print("Mesh is watertight")
        return True
    else:
        # Key "inertia_tensor" does not exist in the measures dictionary
        print("Mesh is not watertight")
        return False

ms.apply_filter("meshing_isotropic_explicit_remeshing", adaptive = True, checksurfdist = False)
# Check number of vertices and faces
print(ms.current_mesh().vertex_number())
print(ms.current_mesh().face_number())
ms.apply_filter("generate_resampled_uniform_mesh", cellsize = pymeshlab.PercentageValue(1.5), mergeclosevert = True, multisample = True)
# Check if mesh is watertight
check_water_tightness(ms)

