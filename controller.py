import vmxparser, os, shlex, sys
from shutil import copyfile

#TODO
# Wtf is the Ruby interface
# Figure out how/where to store templates  VM's and .vmx's currently in use.
# Running VM: vmrun - http://www.vi-toolkit.com/wiki/index.php/Vmrun#:~:text=vmrun%20is%20a%20command%20line,program%20in%20the%20guest%2C%20etcetera.
# Powering off VM: see above
#
# Taking arguments - can parse, need format
# 

##############################################################
# parsing the .vmx files using "vmxparser" into a dictionary #
##############################################################
#yoinked from vmxparser: https://pypi.org/project/vmxparser/

#MUST INPUT OPEN()'D FILE
def parse(file):
    vmx_data = {}
    fileobj = file

    for line in fileobj:
        if line.startswith('#'):
            continue
        key, value = map(str.strip, line.split('=', 1))
        vmx_data[key] = ' '.join(shlex.split(value)) 
            
    return vmx_data

#MUST INPUT OPEN()'D FILE
def save(vmx_data, file):
    fileobj = file

    for key, value in vmx_data.items():
        fileobj.write(key)
        fileobj.write(' = ')
        fileobj.write('"%s"\n' % value.replace('"', '\\"'))

# parsing the .vmx file
#TODO read specific .vmx file, currently testing using .vmx in cwd
with open(os.path.join('./TEMPLATES/', 'UbuntuJavaTemplate.vmx')) as file:
    vmxDict = parse(file)
# for x, y in vmxDict.items():
#     print(x + ' = "' + y + '"')


# test copying template to fake storage, editing copied file
copyfile(os.path.join('./TEMPLATES/', 'UbuntuJavaTemplate.vmx'), os.path.join('./STORAGE/', 'UbuntuJavaTemplateCOPIED.vmx'))
with open(os.path.join('./STORAGE/', 'UbuntuJavaTemplateCOPIED.vmx'), "w") as file:
    vmxDict["RemoteDisplay.vnc.port"] = "589999999"
    save(vmxDict, file)

print(sys.argv)