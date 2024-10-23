import pymeshlab
import subprocess
import json
import time
from mesh_processors import check_water_tightness as cwt
from mesh_processors import repair_mesh

def batch_repair(inpath, outpath, attempts_n, success_json = "list_success.json", failure_json = "list_failure.json"):
    # Import dictionary from a json file
    with open(outpath + "list_error.json", "r") as file:
        meshes = json.load(file)
    print(f"Number of meshes to repair: {len(meshes)}")
    
    SUCCESS = {}
    FAILURE = {}
    count = 1
    
    for key in meshes.keys():
        file_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
        with open(outpath + "log_repair.txt", "a") as job_log:
            job_log.write(f"\nCount {count}. Mesh {key} repair started.\nRepair s time: {file_start_time}.\n")
        
        for i in range(attempts_n):
            cellsize_p = 1.5 + i * 0.25
            try:
                result = subprocess.run(
                    ["python3", "-c", f"import mesh_processors; mesh_processors.repair_mesh('{inpath}', '{key}', '{outpath}', {cellsize_p})"],
                    capture_output=True, text=True
                )
            except subprocess.CalledProcessError:
                with open(outpath + "log_repair.txt", "a") as job_log:
                    job_log.write(f"Attempt {i + 1} encountered an error for mesh {key}.\n\n")
            
            if result.stdout == "good\n":
                file_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
                with open(outpath + "log_repair.txt", "a") as job_log:
                    job_log.write(f"Success. Attempt {i + 1}.\nRepair e time: {file_end_time}.\n\n")
                repaired_file = key.replace(".stl", "_repaired.stl")
                SUCCESS[repaired_file] = cellsize_p
                break
            else:
                file_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
                with open(outpath + "log_repair.txt", "a") as job_log:
                    job_log.write(f"Attempt {i + 1} failed for mesh {key}.\nRepair e time: {file_end_time}.\n\n")
                if i == attempts_n - 1:
                    FAILURE[key] = cellsize_p
        
        count += 1
    
    with open(outpath + success_json, "w") as list_success:
        json.dump(SUCCESS, list_success)
    with open(outpath + failure_json, "w") as list_failure:
        json.dump(FAILURE, list_failure)


#################################################
#inpath = "Thingi10K/raw_meshes/Batch2/"
#outpath = "Thingi10K/raw_meshes/Batch2_results/"
#attempts_n = 3
#batch_repair(inpath, outpath, attempts_n)