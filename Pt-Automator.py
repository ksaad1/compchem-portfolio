import numpy as np
import pandas as pd

filename = "./output"
fileX = open(filename, 'r')
file = fileX.readlines()

distLine = 0
for line in file:
    if "distribution of aqueous species" in line:
        distLine = file.index(line)
    if " +" in line:
        line = line.replace(" +", "+")
    if " -" in line:
        line = line.replace(" -", "-")

speciesStart = distLine + 2
speciesEnd = speciesStart+2+27-1
speciesRawTable = file[speciesStart:speciesEnd]
speciesRawTable.remove(file[speciesStart+1])

for line in speciesRawTable:
        if " +" in line:
            #print("gapped plus found")
            speciesRawTable[speciesRawTable.index(line)] = line.replace(" +", "+")
for line in speciesRawTable:
        if " -" in line:
            #print("gapped minus found")
            speciesRawTable[speciesRawTable.index(line)] = line.replace(" -", "-")

speciesTable = np.array(speciesRawTable)

newfile = open("./species_list.dat", "w+")
newfile.write("species molal_conc log_conc log_g activity log_act\n")
for line in speciesTable[1:]:
    newfile.write(str(line))
newfile.close()

speciesData = pd.read_csv("./species_list.dat", sep='\s+')
PtIndices = []
for species in speciesData['species']:
    if "PT" in species:
        PtIndex = list(speciesData[speciesData['species']==species].index.values)
        #print(PtIndex)
        PtIndices.append(PtIndex[0])
        
PtSpecies = speciesData.iloc[PtIndices]

for line in file:
    if ("PT++" in line) and ("tot conc, molal" in line):
        print("found total conc of Pt")
        numLoc = str(line).index(".")
        Pt_tot = float(str(line)[numLoc:numLoc+10])
        print(Pt_tot)
    if ("CL-" in line) and ("tot conc, molal" in line):
        #print(file.index(line))
        print("found total conc of Cl")
        numLoc = str(line).index(".")
        Cl_tot = float(str(line)[numLoc:numLoc+10])
        print(Cl_tot)
        break

for line in file:
    if "tempc=" in line:
        #print(file.index(line))
        print("found temperature")
        numLoc = str(line).index(".")
        temp = float(str(line)[numLoc:numLoc+10])
        print(str(temp)+" C")
        break

PtSpecies["temp"] = PtSpecies["log_conc"] - PtSpecies["log_conc"] + temp
PtSpecies["Cl_tot"] = PtSpecies["log_conc"] - PtSpecies["log_conc"] + Cl_tot
PtSpecies["Pt_tot"] = PtSpecies["log_conc"] - PtSpecies["log_conc"] + Pt_tot

filename_csv = "./AutomatorTest/Pt_speciation_"+str(temp)+"_C"+"_mPt_"+str(Pt_tot)+"_mCl_"+str(Cl_tot)+".csv"
filename_eq3out = "./AutomatorTest/eq3_out_"+str(temp)+"_C"+"_mPt_"+str(Pt_tot)+"_mCl_"+str(Cl_tot)
print(filename_csv)
PtSpecies.to_csv(filename_csv, sep=",", index=None)

outfile = open(filename_eq3out, 'w+')
for line in file:
    outfile.write(line)
outfile.close()
fileX.close()

#print("found total conc of Pt")
#print(Pt_tot)
#print("found total conc of Cl")
#print(Cl_tot)
#print("found temperature")
#print(str(temp)+" C")
#print("\n Normal Exit")