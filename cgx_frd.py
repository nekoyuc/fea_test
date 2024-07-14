import json
import os

with open('config.json') as f:
    config = json.load(f)

file_path = config['file_path']
frd_file = file_path.split("/")[-1].replace(".stl", "") + ".frd"
os.system("cgx " + frd_file)