import pymeshlab
import json
from mesh_processors import check_water_tightness as cwt


path = "Thingi10K/selected/"

# Import dictionary from a json file
with open(path + "list_error.json", "r") as file:
    meshes = json.load(file)

attempts = 3
print(meshes)
SUCCESS = {}
FAILURE = {}

for key in meshes.keys():
    file_path = path + key
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)

    for i in range(attempts):
        ms.apply_filter("meshing_isotropic_explicit_remeshing", adaptive = True, checksurfdist = False)
        cellsize_p = 1.5 + i * 0.25
        ms.apply_filter("generate_resampled_uniform_mesh", cellsize = pymeshlab.PercentageValue(cellsize_p), mergeclosevert = True, multisample = True)
        if cwt(ms):
            with open(path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Mesh {key} repaired successfully at attempt {i + 1}.\n\n")
            repaired_file = key.replace(".stl", "_repaired.stl")
            SUCCESS[repaired_file] = cellsize_p
            ms.save_current_mesh(path + repaired_file)
            break
        else:
            with open(path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Attempt {i + 1} failed for mesh {key}.\n\n")
            if i == attempts - 1:
                FAILURE[key] = cellsize_p
    ms.clear()

with open(path + "list_success.json", "w") as list_success:
    json.dump(SUCCESS, list_success)
with open(path + "list_failure.json", "w") as list_failure:
    json.dump(FAILURE, list_failure)