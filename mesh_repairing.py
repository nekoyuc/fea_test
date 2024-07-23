import pymeshlab
import subprocess
import json
from mesh_processors import check_water_tightness as cwt
from mesh_processors import repair_mesh

mesh_path = "Thingi10K/raw_meshes/Batch1/"
result_path = "Thingi10K/raw_meshes/Batch1_results/"

# Import dictionary from a json file
with open(result_path + "list_error.json", "r") as file:
    meshes = json.load(file)

attempts_n = 3
print(meshes)
SUCCESS = {}
FAILURE = {}

for key in ["1087143.stl", "1087134.stl", "195700_.stl", "1120764.stl"]:
    print(f"\nfile {key} repair attempt starts")
    for i in range(attempts_n):
        cellsize_p = 1.5 + i * 0.25
        try:
            result = subprocess.run(["python3", "-c", f"import mesh_processors; mesh_processors.repair_mesh('{mesh_path}', '{key}', '{result_path}', {cellsize_p})"], capture_output=True, text=True)
            print(f"{key} file " + "stdout: " + f"{result.stdout}")
        except subprocess.CalledProcessError:
            print(f"{key} file " + "Error")
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Attempt {i + 1} encountered an error for mesh {key}.\n\n")
        
        if result.stdout == "good\n":
            print(f"{key} file " + "repaired successfully")
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Mesh {key} repaired successfully at attempt {i + 1}.\n\n")
            repaired_file = key.replace(".stl", "_repaired.stl")
            SUCCESS[repaired_file] = cellsize_p
            break
        else:
            print(f"{key} file " + f"repair attempt {i} failed")
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Attempt {i + 1} failed for mesh {key}.\n\n")
            if i == attempts_n - 1:
                FAILURE[key] = cellsize_p

'''
#for key in meshes.keys():
for key in ["1087143.stl", "1087134.stl"]:
    file_path = mesh_path + key
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)
    
    print(f"file {key} repair attempt starts")

    for i in range(attempts_n):
        cellsize_p = 1.5 + i * 0.25

        
        viability = repair_subprocess(file_path, cellsize_p)
        if viability == False:
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Attempt {i + 1} for mesh {key} not viable.\n\n")
                FAILURE[key] = cellsize_p
            continue
        

        ms.apply_filter("meshing_isotropic_explicit_remeshing", adaptive = True, checksurfdist = False)
        print("mesh remeshed")
        ms.apply_filter("generate_resampled_uniform_mesh", cellsize = pymeshlab.PercentageValue(cellsize_p), mergeclosevert = True, multisample = True)
        print("mesh processed")
        
        if cwt(ms):
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Mesh {key} repaired successfully at attempt {i + 1}.\n\n")
            repaired_file = key.replace(".stl", "_repaired.stl")
            SUCCESS[repaired_file] = cellsize_p
            ms.save_current_mesh(result_path + repaired_file)
            print("mesh saved successfully")
            break
        else:
            with open(result_path + "log_repair.txt", "a") as job_log:
                job_log.write(f"Attempt {i + 1} failed for mesh {key}.\n\n")
            if i == attempts_n - 1:
                FAILURE[key] = cellsize_p
            print("mesh repair failed")

    ms.clear()
    print("mesh cleared\n")
'''

with open(result_path + "list_success.json", "w") as list_success:
    json.dump(SUCCESS, list_success)
with open(result_path + "list_failure.json", "w") as list_failure:
    json.dump(FAILURE, list_failure)
