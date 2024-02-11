import numpy as np
import pandas as pd
import os

filename = "./input"
fileX = open(filename, 'r')
file = fileX.readlines()

temp_line = 0
pt_conc_line = 0
cl_conc_line = 0

for line in file:
    if "tempc=" in line:
        templine = file.index(line)
    if "data file master species= PT++" in line:
        pt_conc_line = file.index(line)
    if "data file master species= CL-" in line:
        cl_conc_line = file.index(line)

#print(templine, pt_conc_line, cl_conc_line)
fileX.close()

temp_inputs = [300,350,400,450,500,550,600]
cl_inputs = [1e0,1e-1,1e-2,1e-3,1e-4,0.00001,1e-6,1e-7,1e-8,1e-9,1e-10]
pt_inputs = [1e0,1e-1,1e-2,1e-3]
for pt in pt_inputs:
    for cl in cl_inputs:
        for temp in temp_inputs:
            file[templine] = file[templine].replace(file[templine], 
                "     tempc=         "+str(int(temp))
                +".\n")
            file[cl_conc_line+2] = file[cl_conc_line+2].replace(
                file[cl_conc_line+2], "   jflag=  0   csp= "+
                str("0."+(int(np.log10(1/cl)-1))*"0"+"1\n"))
            file[pt_conc_line+2] = file[pt_conc_line+2].replace(
                file[pt_conc_line+2], "   jflag=  0   csp= "+
                str("0."+(int(np.log10(1/pt)-1))*"0"+"1\n"))
            
            inputfile = open("./input", 'w')
            for line in file:
                inputfile.write(line)
            inputfile.close()
            
            os.system("./eq3")
            os.system("python ./Pt-Automator.py")