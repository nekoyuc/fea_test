import os
import subprocess
import gmsh
import json
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi
#from ccx_inp import ccx_inp as ccx
#from cgx_frd import cgx_frd as cf

inpath = "Thingi10K/raw_meshes/"
outpath = "Thingi10K/processed_meshes/"
ERRORS = {}

def get_files(inpath, method = "directory", json_name = ""):
    if method == "directory":
        files = os.listdir(inpath)
        # delete files that do not end with ".stl"
        for file in files:
            if not file.endswith(".stl"):
                files.remove(file)
        return files
    elif method == "json":
        with open(inpath + json_name, "r") as file:
            files_list = json.load(file)
        files = []
        for key in files_list.keys():
            files.append(key)
        return files
    elif method == "custom":
        files = []
        return files

files = get_files(inpath, method = "directory", json_name = "list_success.json")

for file in files:
    file_path = inpath + file
    with open("trials.txt", "w") as log:
        log.write(f"Started file {file}.\n")
    try:
        # Process mesh with gmsh
        inp_file_path = mp(file, inpath, outpath)
        ## If mp encounters an error, jump to the except block
        # modify the .inp file generated by mp
        mi(inp_file_path)
        inp_file_path = inp_file_path.replace(".inp", "")
        command = "ccx " + inp_file_path
        with open(outpath + file + "_output.txt", "w") as outfile:
            # Run Calculix with the modified .inp file
            subprocess.run(f"{command} | tail -n 6", shell = True, stdout = outfile, stderr = outfile)
        with open(outpath + file + "_output.txt", "r") as outfile:
            # if the sixth from the last line of the output file does not contain "Job finished", write an error message to the error log
            output_lines = outfile.readlines()
            if not "Job finished" in output_lines[-6]:
                ERRORS[file] = output_lines
                with open(outpath + "log_job.txt", "a") as log_job:
                    log_job.write(f"Error in Calculix analysis for file {file}:\n")
                    log_job.write("".join(output_lines) + "\n\n")
                continue
            else:
                with open(outpath + "log_job.txt", "a") as log_job:
                    log_job.write(f"File {file} processed successfully.\n\n")
    except Exception as e:
        gmsh.finalize()
        ERRORS[file] = str(e)
        with open(outpath + "log_job.txt", "a") as log_job:
            log_job.write(f"Error processing file {file}: {str(e)}\n\n")
        continue

# Export ERRORS to a json file
with open(outpath + "list_error.json", "w") as list_error:
    json.dump(ERRORS, list_error)