import os, sys
from time import sleep
from shlex import split
from shutil import move, rmtree, make_archive
from zipfile import ZipFile
from glob import glob
from pathlib import Path

#TODO
# Wtf is the Ruby interface
# Figure out how/where to store templates  VM's and .vmx's currently in use.
#
# 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# parsing the .vmx files using "vmxparser" into a dictionary  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# yoinked from vmxparser: https://pypi.org/project/vmxparser/
#MUST INPUT OPEN()'D FILE
# parses .vmx file into a dictionary
def parse(file):
    vmx_data = {}
    if isinstance(file, str):
        fileobj = open(file)
    else:
        fileobj = file
    
    try:
        for line in fileobj:
            if line.startswith('#'):
                continue
            key, value = map(str.strip, line.split('=', 1))
            vmx_data[key] = ' '.join(split(value)) 
    finally:
        if fileobj is not file:
            fileobj.close()
    return vmx_data

#MUST INPUT OPEN()'D FILE
# saves dict "vmx_data" to file "file"
def save(vmx_data, file):
    if isinstance(file, str):
        fileobj = open(file, 'r+')
    else:
        fileobj = file

    for key, value in vmx_data.items():
        fileobj.write(key + ' = ' + '"%s"\n' % value.replace('"', '\\"'))



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ~~   different modes to run inside pseudo switch case    ~~ #
# VM should be created in SSD (RUNNING for now) where it can  #
# be started/stopped. The VM will stay here until Ruby sends  #
# sends move command (moves from RUNNING/SSD to STORAGE/HDD)  #
# and later compress command (compress VM and delete VM dir)  #
#                                                             #
# TODO add others if needed                                   #
# NEED TO PARSE VMTYPE TO POINT TO OTHER VM TEMPLATES         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#creates the specified VM at vmDir of type vmType
def createvm(vmDir, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()

    # creates directory for vmDir if doesn't exist
    Path(vmDir).mkdir(parents=True, exist_ok=True)

    # TODO Here will go the code that parses the vmType into a specific directory 
    # that points to the template zip

    # extracts template to created folder    
    with ZipFile('./TEMPLATES/UbuntuJavaTemplateTEST.zip', 'r') as zip_ref:
        zip_ref.extractall(path=os.path.dirname(vmDir))

# configures the VNC port correctly and launches the specified VM
def startvm(vmDir, vmType, vncPort):
    if len(sys.argv) < 5:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 5:
        print("Too many arguments.")
        exit()

    # handles directory error
    if not os.path.exists(vmDir):
        print("That VM doesn't exist! Check your directory or run '-createvm' first.")
        exit()

    # reads .vmx to file to be edited
    vmxPath = glob(os.path.join(vmDir, '*.vmx'))[0]
    with open(vmxPath, 'r+') as file:
        vmxDict = parse(file)
    # configures VNC port to be vncPort and saves it
    vmxDict["RemoteDisplay.vnc.port"] = vncPort
    # stops the annoying "I copied it" window from popping up 
    vmxDict["uuid.action"] = 'keep'

    save(vmxDict, vmxPath)   

    # launches the VM at vmxPath
    os.system(f'vmrun start {vmxPath}') 

# stops specifiec VM
def stopvm(vmDir):
    if len(sys.argv) < 3:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 3:
        print("Too many arguments.")
        exit()

    #finds the .vmx and stops the VM
    vmxPath = glob(os.path.join(vmDir, '*.vmx'))[0]    
    os.system(f'vmrun stop {vmxPath}') 
    sleep(1)

# compresses folder vmDir
def compressvm(vmDir):
    if len(sys.argv) < 3:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 3:
        print("Too many arguments.")
        exit()
        
    # dirParts = list(Path(vmDir).parts)
    # targ = os.path.join(*dirParts)

    # zips up folder vmDir
    make_archive(vmDir, 'zip', os.path.dirname(vmDir))
    # removes redundant VM at vmDir
    rmtree(vmDir)

# moves vmDir to tarDir. Shocking, I know
def movevm(vmDir, tarDir):
    move(vmDir, tarDir)
    if len(os.listdir(os.path.dirname(os.path.dirname(vmDir)))) == 0:
        rmtree(os.path.dirname(os.path.dirname(vmDir)))

#lame ass switch case
def switch(arg):
    if arg == "-startvm":
        return startvm(sys.argv[2], sys.argv[3], sys.argv[4])
    elif arg == "-stopvm":
        return stopvm(sys.argv[2])
    elif arg == "-createvm":
        return createvm(sys.argv[2], sys.argv[3])
    elif arg == "-compressvm":
        return compressvm(sys.argv[2])
    elif arg == "-movevm":
        return movevm(sys.argv[2], sys.argv[3])
    else:
        print(f'"{arg}" is not a valid command!')
        exit()
    
switch(sys.argv[1])
#print(os.path.join('.\\TEMPLATES', glob('.\\TEMPLATES\\*.zip')[1]))
# ARGS: -type targetVM targetVMType VNCPort
#        [1]    [2]        [3]        [4]