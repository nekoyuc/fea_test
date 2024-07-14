import json
import os
import subprocess

#with open('config.json') as f:
#    config = json.load(f)

#file_path = config['file_path']
def ccx_inp(inp_file):
    inp_file = inp_file.replace(".inp", "")
    command = "ccx " + inp_file
    os.system(command)
    return inp_file + ".frd"