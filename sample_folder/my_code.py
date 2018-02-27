import numpy as np
import json

with file('params.json', 'r') as infile:
    params = json.load(infile)

np.save(params['a_string'], params['mysterious_parameter']*np.array(params['interesting_parameter']))