import os
import subprocess
import gmsh
from mesh_processing import mesh_processing as mp
from modify_inp import modify_inp as mi
from ccx_inp import ccx_inp as ccx
from cgx_frd import cgx_frd as cf

path = "Thingi10K/selected/"
ERRORS = []

for _, _, files in os.walk(path):
    for file in files:
        # if file name does not end with ".stl", skip the file
        if not file.endswith(".stl"):
            continue
        file_path = path + file
        try:
            inp_file = mp(file_path)
            mi(inp_file)
            inp_file = inp_file.replace(".inp", "")
            command = "ccx " + inp_file
            with open(inp_file + "_output.txt", "w") as outfile:
                subprocess.run(f"{command} | tail -n 6", shell = True, stdout = outfile, stderr = outfile)
                
            with open(inp_file + "_output.txt", "r") as outfile:
                # if the sixth from the last line of the output file does not contain "Job finished", write an error message to the error log
                output_lines = outfile.readlines()
                if not "Job finished" in output_lines[-6]:
                    ERRORS.append([file_path, output_lines])
                    with open(path + "error_log.txt", "a") as error_log:
                        error_log.write(f"Error processing file {file_path}:\n")
                        error_log.write("".join(output_lines) + "\n\n")
                    continue
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            ERRORS.append([file_path, str(e)])
            with open(path + "error_log.txt", "a") as error_log:
                error_log.write(f"Error processing file {file_path}: {str(e)}\n\n")
            continue
        #frd_file = ccx(inp_file)
        #cf(frd_file)

print("Error log:")
print(ERRORS)