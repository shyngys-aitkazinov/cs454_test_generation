import random
from pathlib import Path
import os
import json

def write_in_file (chromosome):
    file_name = "tes_coverage" + ".py" 
    folder_path = str(Path().absolute()) 
    path = os.path.join(folder_path,file_name)
    f = open( path, "w")
    f.write("import coverage\n")
    f.write("cov = coverage.Coverage() \n")
    f.write("cov.start()\n")


    for i in chromosome:
        f.write(i + "\n")
    
    f.write("cov.stop()\n")
    f.write("cov.save()\n")
    f.write("cov.json_report()\n")
    f.close()
    exec(open(file_name).read())
    with open('coverage.json', 'r') as f:
        data = json.load(f)
        return (data['files']['example.py']['summary']['percent_covered'])


# chom = ['import example', 'x = 4', 'y = 916', 'z = 487', 'v0 = example.triangle( x, y, z )']

# write_in_file(chom)