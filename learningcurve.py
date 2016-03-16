import pandas as pd
import numpy as np
from subprocess import call

Npts = 2

from random import randint

for i in range(Npts):
    size = randint(500,15898)

    with open("script{0}.sh".format(i), "w") as of:
        of.write("#!/bin/bash\n")
        of.write("#PBS -l nodes=1:ppn=1\n")
        of.write("#PBS -q workq\n")
        of.write("#PBS -r n\n")
        of.write("#PBS -l walltime=12:00:00\n")
        of.write("#PBS -N machinelearningdata\n")
        of.write("cd $PBS_O_WORKDIR\n")
        of.write("module load gcc/4.9.2\n")
        of.write("source /mnt/raid-cita/dtamayo/p2/bin/activate\n")
        of.write("python /mnt/raid-cita/dtamayo/NCAAbasketball/rf.py {0}\n".format(size))
        
        call("chmod u=rwx script{0}.sh".format(i), shell=True)

with open("rfscript", "w") as of:
    of.write("#!/bin/bash\n")
    for i in range(Npts):
        of.write("qsub script{0}.sh\n".format(i))

    call("chmod u=rwx rfscript", shell=True)
    
