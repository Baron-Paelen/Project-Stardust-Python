import os, shlex, sys, shutil, zipfile

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
            vmx_data[key] = ' '.join(shlex.split(value)) 
    finally:
        if fileobj is not file:
            fileobj.close()
    return vmx_data

#MUST INPUT OPEN()'D FILE
# Saves dict "vmx_data" to file "file"
def save(vmx_data, file):
    if isinstance(file, str):
        fileobj = open(file)
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

def createvm(vmDir, vmType):
    
    #TODO need to know how ot take in parameter
    os.mkdir(vmDir)
    with zipfile.ZipFile(os.path.join('./TEMPLATES/', 'UbuntuJavaTemplate.zip'), 'r') as zip_ref:
        zip_ref.extractall(vmDir)


def startvm(vmDir, vmType, vncPort):
    if not os.path.exists(vmDir):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + os.path.exists(vmDir))
        createvm(vmDir, vmType)
    #TODO need to know what parameters we gon use
    with open(os.path.join(vmDir, "")) as file:
        vmxDict = parse(file)
    vmxDict["RemoteDisplay.vnc.port"] = vncPort
    save(vmxDict, os.join(vmDir, vmType + ".vmx"))    

def stopvm(vmDir):
    #TODO need ot know what parameters we gon use
    print("nghvkhfkhvjyfkjytfhfkuyrkjykvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    pass

#lame ass switch case
def switch(arg):
    if arg == "-startvm":
        return startvm(sys.argv[2], sys.argv[3], sys.argv[4])
    elif arg == "stopvm":
        return stopvm(sys.argv[2])
    else:
        print(f'"{arg}" is not a valid command!')
        exit()
    
switch(sys.argv[1])
