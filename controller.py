import os, shlex, sys, shutil

#TODO
# Wtf is the Ruby interface
# Figure out how/where to store templates  VM's and .vmx's currently in use.
# Running VM: vmrun - http://www.vi-toolkit.com/wiki/index.php/Vmrun#:~:text=vmrun%20is%20a%20command%20line,program%20in%20the%20guest%2C%20etcetera.
# Powering off VM: see above
#
# Taking arguments - can parse, need format
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
# stopvm - read: above                                        #
#                                                             #
#                                                             #
#TODO add others if needed                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def startvm():
    #TODO need to know what parameters we gon use
    print("RWERWERWERWERERWER")
    pass

def stopvm():
    #TODO need ot know what parameters we gon use
    print("STOPP IT ")
    pass

#pseudo switch case
def switch(arg):
    statement = {
        "-startvm" : startvm(),
        "-stopvm" : stopvm()
    }


if not os.path.exists(sys.argv[2]): 
    print(f"Directory not found: {sys.argv[2]}")
    exit()
if os.path.exists(sys.argv[3]): 
    print(f"Directory already exists: {sys.argv[2]}")
    exit()


shutil.copytree(os.path.join(sys.argv[2]), os.path.join(sys.argv[3]))

switch(sys.argv[1])