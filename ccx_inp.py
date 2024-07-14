import json
import os
import subprocess

with open('config.json') as f:
    config = json.load(f)

# print all file names in the "Thingi10K/selected test meshes" folder
for root, dirs, files in os.walk("Thingi10K/selected test meshes"):
    for file in files:
        print(file)

'''
file_path = config['file_path']
inp_file = file_path.split("/")[-1].replace(".stl", "")
command = "ccx " + inp_file
os.system(command)

# Get the last 6 lines of the terminal output and put them in a text file
with open(inp_file + "_output.txt", "w") as outfile:
    subprocess.run(f"{command} | tail -n 6", shell = True, stdout = outfile, stderr = outfile)
'''