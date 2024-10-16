import os
import subprocess
import gmsh
import json
from collections import deque
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi
import subprocess
import time
#from ccx_inp import ccx_inp as ccx
#from cgx_frd import cgx_frd as cf

def get_files(path, method = "directory", json_name = ""):
    if method == "directory":
        files = os.listdir(path)
        # delete files that do not end with ".stl"
        for file in files:
            if not file.endswith(".stl"):
                files.remove(file)
        return files
    elif method == "json":
        with open(path + json_name, "r") as file:
            files_list = json.load(file)
        files = []
        for key in files_list.keys():
            files.append(key)
        return files
    elif method == "custom":
        files = []
        return files
    
def write_to_log(stl_file, log_file, count, message):
    with open(log_file, "a") as log:
        log.write(f"Count {count}, {stl_file} results:\n")
        log.write(message)

def mp_subprocess(file, inpath, outpath, count, ERROR, message):
    t = 100
    try:
        start_time = time.time()  # Record the start time
        result = subprocess.run(
            ["python3", "-c", f"import mesh_processors; mesh_processors.mesh_processing('{file}', '{inpath}', '{outpath}')"],
            capture_output=True,
            timeout = t  # Set the timeout value in seconds
        )
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        output = result.stdout
        #print(str(file) + " finished mp subprocess")
        if result.returncode == 0:
            file_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
            message += f"MP e time: {file_end_time}\n"
            message += f"MP success.\nMP processing time: {execution_time}\n\n"
            write_to_log(file, outpath + "log_job.txt", count, message)
            return True
        else:
            #print("Error\n")
            # Take the last 6 lines of output
            output_lines = output.splitlines()
            output_lines = output_lines[-6:]
            ERROR[file] = message
            file_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
            message += f"MP e time: {file_end_time}\n"
            message += f'Error processing {file}: {output_lines}\n' + f'MP processing time: {execution_time}\n\n'
            write_to_log(file, outpath + "log_job.txt", count, message)
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except subprocess.TimeoutExpired:
        #print("Timeout\n")
        message += f'Timeout processing {file} after {t} seconds\n\n'
        ERROR[file] = message
        write_to_log(file, outpath + "log_job.txt", count, message)
        return None
    except subprocess.CalledProcessError as e:
        #print("exception\n")
        return None

def batch_execute(inpath, outpath, method, json_name):
    count = 1
    ERRORS = {}
    files = get_files(inpath, method = method, json_name = json_name)
    total = len(files)
    print(f"Total number of files to process: {total}")
    for file in files:
        with open("trials.txt", "w") as log:
            log.write(f"Total number of files: {total}\nStarted file number {count}, {file}.\n")
        message = ""
        file_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
        message += f"MP s time: {file_start_time}\n"
        result = mp_subprocess(file, inpath, outpath, count, ERRORS, message)
        if result:
            inp_file_path = outpath + file
            inp_file_path = inp_file_path.replace(".stl", ".inp")
            mi(inp_file_path)
            inp_file_path = inp_file_path.replace(".inp", "")

            command = "ccx " + inp_file_path

            ccx_start_time = time.time()
            with open(outpath + "_ccx_output.txt", "w") as outfile:
                subprocess.run(f"{command} | tail -n 6", shell=True, stdout=outfile, stderr=outfile)
            ccx_end_time = time.time()
            ccx_execution_time = ccx_end_time - ccx_start_time

            with open(outpath + "_ccx_output.txt", "r") as outfile:
                output_lines = outfile.readlines()
                if not "Job finished" in output_lines[-6]:
                    ERRORS[file] = output_lines
                    ccx_message = "Calculix\n" + "".join(output_lines) + f'\nCCX processing time: {ccx_execution_time}\n\n'
                else:
                    ccx_message = "Calculix analysis completed successfully." + f'\nCCX processing time: {ccx_execution_time}\n\n'

            write_to_log(file, outpath + "log_job.txt", count, ccx_message)
        count = count + 1

    # Export ERRORS to a json file
    with open(outpath + "list_error.json", "w") as list_error:
        json.dump(ERRORS, list_error)


###################################################
###################################################
### Modify inpath, outpath, and method as needed ###
#inpath = "Thingi10K/raw_meshes/Batch2_results/"
#outpath = "Thingi10K/raw_meshes/Batch2_results/"
#method = "json" # "directory", "json", "custom"
#json_name = "list_success.json"
#batch_execute(inpath, outpath, method, json_name)
