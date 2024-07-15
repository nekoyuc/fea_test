import os
import json
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi

mp("Thingi10K/selected/35269_repaired.stl")
#mi("Thingi10K/selected/36075_repaired.inp")

# Get all files in the directory
path = "Thingi10K/selected/"
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

#files = get_files(path, method = "json", json_name = "list_success.json")
#print(files)

#with open("Thingi10K/selected/list_error.json", "r") as file:
#    meshes = json.load(file)
#path = "Thingi10K/selected/"
#print(meshes)