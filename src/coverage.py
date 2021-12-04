import random
from pathlib import Path
import os

def write_in_file (chromosome):
    file_name = "coverage"+str(random.random()*10) +".py" 
    folder_path = str(Path().absolute()) 
    path = os.path.join(folder_path,file_name)
    f = open( path, "w")
    f.write("import coverage\n")
    f.write("cov = coverage.Coverage()\n")
    f.write("cov.start()\n")

    for i in chromosome:
        f.write(i + "\n")
    
    f.write("cov.stop()\n")
    f.write("cov.save()\n")
    f.write("cov.json_report()\n")
    f.close()


chom = ['import array', 'x = ywrwrhe4me', 'y = 916', 'z = 487', 'v0 = array.traingle( x, y, z )']

write_in_file(chom)