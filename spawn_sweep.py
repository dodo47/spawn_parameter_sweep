# Script used to perform parameter scans of arbitrary numerical models.
# A single simulation should be fully specified with parameters given by a dictionary to use this script.
# Author: Dominik Dold
import os 
import json 
from shutil import copyfile

# FUNCTIONS TO CREATE PARAM FILES+FOLDERS+START ALL SIMULATIONS
def turn_dict_to_list(scan_params):
    return scan_params.keys(), scan_params.values()

def create_combs(slist, id, coll_list):
    if id == len(slist):
        return [coll_list]
    else:
        total_list = []
        for i in range(len(slist[id])):
            total_list += create_combs(slist, id+1, coll_list+[slist[id][i]])
        return total_list

def create_path(param_names, values):
    path = ''
    for i in range(len(param_names)):
        path += param_names[i] + '_' + str(values[i]) + '--'
    for syms in [' ', '[', ']']:
    	path = path.replace(syms, '')
    path = path.replace(',', '_')
    return path[:-2]

def copy_files(files_path, sim_path):
    for paths in files_path:
        copyfile(paths, sim_path+'/'+get_file_name(paths))

def set_params(params, param_names, values):
    for i in range(len(param_names)):
        params[param_names[i]] = values[i]

def get_file_name(path):
    for i in range(len(path)):
        if path[-i] == '/':
            return path[-i+1:]
    return path

# PARAM DICT DESCRIBING A SINGLE SIMULATION
# contains all parameters needed to fully characterize a simulation run
params = {
    'some_parameter': 42.,
    'another_parameter': True,
    'interesting_parameter': [1,2,3],
    'mysterious_parameter': 0.1,
    'a_string': 'iamastring',
}

# PARAMS TO BE SCANNED
# all parameters + the values the simulation should be run with
# parameters that stay constant over all simulations are not listed here but should be set in params = {}
scan_params = {
    "interesting_parameter": [[1,2,3], [2,3,4]],
    "mysterious_parameter": [0.1, 0.2],
    "a_string": ['amiastring', 'iamnostring'],
}

# LOCATION OF SIM. SCRIPTS + SIM. START 
# for every set of parameters, this script will create a folder and copy the files listed in files_to_copy there
# the param-dict for the simulations are also saved in this folder
# sim_start_command is the terminal command used to start the simulation script
files_to_copy = ['sample_folder/my_code.py', 'sample_folder/start_sim.sh']
sim_start_command = "bash start_sim.sh"

# MAIN FUNCTION
if __name__ == "__main__":
    param_names, param_values = turn_dict_to_list(scan_params)
    param_values = create_combs(param_values, 0, [])
    for vals in param_values:
        pathname = create_path(param_names, vals)
        os.system("mkdir '"+pathname+"'")
        copy_files(files_to_copy, pathname)
        set_params(params, param_names, vals)
        with file(pathname+'/params.json', 'w') as param_file:
            json.dump(params, param_file)
        os.chdir(pathname)
        os.system(sim_start_command)
        os.chdir("..")