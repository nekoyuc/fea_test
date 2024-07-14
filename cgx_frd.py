import json
import os

#with open('config.json') as f:
#    config = json.load(f)

def cgx_frd(frd_file):
    os.system("cgx " + frd_file)