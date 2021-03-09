import os, sys
from time import sleep
from shlex import split
from shutil import move, rmtree, make_archive
from zipfile import ZipFile
from glob import glob
from pathlib import Path

###############################################################################
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

#################################################################################

runDir = f".{os.sep}RUNNING{os.sep}"
storageDir = f".{os.sep}STORAGE{os.sep}"
templateDir = f".{os.sep}TEMPLATES{os.sep}"

UbunTemplate = "UbuntuJavaTemplate.zip"


#creates the specified VM at vmDir of type vmType
def createvm(vmOwner, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()

    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate
    
    with ZipFile(os.path.join(templateDir, UbunTemplate), 'r') as zip_ref:
        vmDir = os.path.join(runDir, vmOwner, vmType2[:-4])
        # print(vmDir)
        Path(vmDir).mkdir(parents=True, exist_ok=True)  
        zip_ref.extractall(path=os.path.dirname(vmDir))
    

# configures the VNC port correctly and launches the specified VM
def startvm(vmOwner, vmType, vncPort):
    if len(sys.argv) < 5:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 5:
        print("Too many arguments.")
        exit()

    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate
    
    vmDir = os.path.join(runDir, vmOwner, vmType2[:-4])
    print(vmDir)

    # handles directory error
    if not os.path.exists(vmDir):
        print("That VM doesn't exist! Check your directory or run '--createvm' first.")
        exit()

    # reads .vmx to file to be edited
    vmxPath = os.path.join(vmDir, vmType2[0:-4] + '.vmx')
    
    with open(vmxPath, 'r+') as file:
        vmxDict = parse(file)
    # configures VNC port to be vncPort and saves it
    vmxDict["RemoteDisplay.vnc.port"] = vncPort
    # stops the annoying "I copied it" window from popping up 
    vmxDict["uuid.action"] = 'keep'

    save(vmxDict, vmxPath)   

    # launches the VM at vmxPath
    os.system(f'vmrun start {vmxPath}') 

# stops vmOwner's vmType virtual machine
def stopvm(vmOwner, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()

    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate

    #finds the .vmx and stops the VM
    vmxPath = os.path.join(vmDir, vmType2[0:-4] + '.vmx')    
    os.system(f'vmrun stop {vmxPath}') 
    sleep(1)

# compresses vmOwner's vmType virtual machine and places it in storageDir
def archivevm(vmOwner, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()
        
    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate

    vmDir = os.path.join(runDir, vmOwner, vmType2[:-4])

    # zips up folder vmDir and puts it into the STORAGE location
    # note: make_archive(./dir1, 'zip', dir2) makes a zipped file in '..' with the name of '..'.zip containing the contents of dir2
    make_archive(os.path.join(storageDir, vmOwner, vmType2[:-4]), 'zip', Path(vmDir))

    # removes redundant VM at vmDir
    rmtree(vmDir)

# restores vmOwner's vmType virtual machine and places it in runDir
def restorevm(vmOwner, vmType):
    if len(sys.argv) < 4:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 4:
        print("Too many arguments.")
        exit()

    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate

    if not os.path.isfile(os.path.join(storageDir, vmOwner, vmType2)):
        print(f"That archive does not exist. Check in {storageDir} or create an archive before using this command.")
        exit()
    
    # extracts specified VM from storageDir to runDir
    with ZipFile(os.path.join(storageDir, vmOwner, vmType2)) as file:
        file.extractall(os.path.join(runDir, vmOwner, vmType2[:-4]))

    # removes redendant archive in storageDir
    os.remove(os.path.join(storageDir, vmOwner, vmType2))

# moves vmOwner's vmType virtual machine 
def movevm(vmOwner, vmType, tarDir):
    if len(sys.argv) < 5:
        print("Insufficent arguments.")
        exit()
    if len(sys.argv) > 5:
        print("Too many arguments.")
        exit()

    if (vmType == "Ubuntu"):
        vmType2 = UbunTemplate
    vmDir = os.path.join(runDir, vmOwner, vmType2[:-4])
    move(vmDir, tarDir)

#lame ass switch case
def switch(arg):
    if arg ==   "--startvm":
        return startvm(sys.argv[2], sys.argv[3], sys.argv[4])
    elif arg == "--stopvm":
        return stopvm(sys.argv[2], sys.argv[3])
    elif arg == "--createvm":
        return createvm(sys.argv[2], sys.argv[3])
    elif arg == "--archivevm":
        return archivevm(sys.argv[2], sys.argv[3])
    elif arg == "--restorevm":
        return restorevm(sys.argv[2], sys.argv[3])
    elif arg == "--movevm":
        return movevm(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(f'"{arg}" is not a valid command!')
        exit()
    
print(sys.argv)
print(len(sys.argv))
if(len(sys.argv) > 1):
    switch(sys.argv[1])
else:
    print("Insufficient Arguments")