import os, sys
from time import sleep
from shlex import split
from shutil import move, rmtree
from zipfile import ZipFile
from glob import glob
from pathlib import Path

#TODO
# Wtf is the Ruby interface
# Figure out how/where to store templates  VM's and .vmx's currently in use.
# Running VM: vmrun - http://www.vi-toolkit.com/wiki/index.php/Vmrun#:~:text=vmrun%20is%20a%20command%20line,program%20in%20the%20guest%2C%20etcetera.
# Powering off VM: see above
#
# Taking arguments - can parse, need funcitonality
# 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# parsing the .vmx files using "vmxparser" into a dictionary  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# yoinked from vmxparser: https://pypi.org/project/vmxparser/
#MUST INPUT OPEN()'D FILE
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
# Saves dict "vmx_data" to file "file"
def save(vmx_data, file):
    if isinstance(file, str):
        fileobj = open(file, 'r+')
    else:
        fileobj = file

    for key, value in vmx_data.items():
        fileobj.write(key + ' = ' + '"%s"\n' % value.replace('"', '\\"'))



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# different modes to run inside pseudo switch case            #
# startvm - gee I wonder                                      #
#   createvm - create a VM from template                      #
# stopvm - read: above                                        #
#                                                             #
#                                                             #
# TODO add others if needed                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#creates the specified VM at vmDir of type vmType
def createvm(vmDir, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()

    print("Making dir: " + vmDir + " unzipping template")
    Path(vmDir).mkdir(parents=True, exist_ok=True)

    # TODO Here will go the code that parses the vmType into a specific directory 
    # that points to the template zip
    
    #print(ZipFile('./TEMPLATES/UbuntuJavaTemplateTEST.zip', 'r').namelist())
    with ZipFile('./TEMPLATES/UbuntuJavaTemplateTEST.zip', 'r') as zip_ref:
        #print(zip_ref.namelist())
        zip_ref.extractall(path=os.path.dirname(os.path.dirname(vmDir)))

    vmxPath = glob(os.path.join(vmDir, '*.vmx'))[0]
    with open(vmxPath, 'r+') as file:
        vmxDict = parse(file)
    # stops the annoying "I copied it" window from popping up 
    vmxDict["uuid.action"] = 'keep'
    save(vmxDict, vmxPath)   

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
    save(vmxDict, vmxPath)   

    # launches the VM at vmxPath
    os.system(f'vmrun start {vmxPath}') 

def stopvm(vmDir):
    if len(sys.argv) < 3:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 3:
        print("Too many arguments.")
        exit()
        
    vmxPath = glob(os.path.join(vmDir, '*.vmx'))[0]    
    os.system(f'vmrun stop {vmxPath}') 
    sleep(3)

    peth = Path(vmDir)
    thing = list(peth.parts)
    thing[0] = "STORAGE"
    targ = os.path.join(*thing)
    print(targ)

    move(vmDir, targ)
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
    else:
        print(f'"{arg}" is not a valid command!')
        exit()
    
switch(sys.argv[1])
#print(os.path.join('.\\TEMPLATES', glob('.\\TEMPLATES\\*.zip')[1]))
# ARGS: -type targetVM targetVMType VNCPort
#        [1]    [2]        [3]        [4]