# User Guide

## batch_execution.py

### Description
`batch_execution.py` is a script designed to do linear elastic solid body FEA on a batch of stl files.

### Inputs
- **inpath**: directory where the batch stl files exist.
- **outpath**: directory where the processed inp files, job log, ccx output, and error list exist.
- **method**: 

### BELOW ARE BOILER PLATE CONTENTS TO BE UPDATED###
### Usage
```bash
python batch_execution.py --task_list <path_to_task_list> --mode <execution_mode> --log_file <path_to_log_file>
```

### Example
```bash
python batch_execution.py --task_list tasks.json --mode parallel --log_file execution.log
```

## mesh_repairing.py

### Description
`mesh_repairing.py` is a script used to repair and optimize 3D mesh files.

### Inputs
- **input_mesh**: Path to the input mesh file that needs to be repaired.
- **output_mesh**: Path where the repaired mesh file will be saved.
- **repair_level**: Level of repair to be applied, ranging from `low` to `high`.

### Usage
```bash
python mesh_repairing.py --input_mesh <path_to_input_mesh> --output_mesh <path_to_output_mesh> --repair_level <repair_level>
```

### Example
```bash
python mesh_repairing.py --input_mesh model.obj --output_mesh repaired_model.obj --repair_level high
```
