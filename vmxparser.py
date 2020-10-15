import shlex


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


def strencode(text):
    def iterator():
        for c in text:
            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                yield c
            else:
                yield '|%02X' % ord(c)
    return ''.join(iterator())


def strdecode(text):
    def iterator():
        text_iter = iter(text)
        c = next(text_iter, None)
        while c:
            if c == '|':
                try:
                    hexchr = ''.join([next(text_iter), next(text_iter)])
                except StopIteration as err:
                    raise ValueError('%10s is encoded badly') from err
                yield chr(int(hexchr, 16))
            else:
                yield c
            c = next(text_iter, None)
    return ''.join(iterator())

