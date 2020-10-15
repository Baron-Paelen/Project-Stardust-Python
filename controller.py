import vmxparser, os, shlex




##############################################################
# parsing the .vmx files using "vmxparser" into a dictionary #
##############################################################
#yoinked from vmxparser: https://pypi.org/project/vmxparser/
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
            line = fileobj.readline()
    finally:
        if fileobj is not file:
            fileobj.close()
    return vmx_data


def save(vmx_data, file):
    if isinstance(file, str):
        fileobj = open(file, 'w')
    else:
        fileobj = file
    
    try:
        for key, value in vmx_data.items():
            fileobj.write(key)
            fileobj.write(' = ')
            fileobj.write('"%s"\n' % value.replace('"', '\\"'))
    finally:
        if fileobj is not file:
            fileobj.close()

#TODO read specific .vmx file, currently testing using .vmx in cwd
with open(os.path.join('./', 'UbuntuJavaTemplate.vmx')) as file:
    vmxDict = parse(file)

print(vmxDict)