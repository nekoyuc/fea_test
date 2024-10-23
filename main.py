from batch_execution import batch_execute
from mesh_repairing import batch_repair
import time

inpath = "Thingi10K/raw_meshes/Batch35/"
outpath = "Thingi10K/raw_meshes/Batch35_results/"
method1 = "directory" # "directory", "json", "custom"
method2 = "json" # "directory", "json", "custom"
json_name = "list_success.json"
attempt_n = 3

start_time = time.time()
batch_execute(inpath, outpath, "directory", "") # Process all files in the directory
batch_repair(inpath, outpath, attempt_n, json_name) # Repair meshes that failed the first time
batch_execute(outpath, outpath, "json", json_name) # Process repaired meshes
end_time = time.time()

execution_time = end_time - start_time
with open(outpath + "log_job.txt", "a") as log:
    log.write(f"Total execution time: {execution_time} seconds\n")