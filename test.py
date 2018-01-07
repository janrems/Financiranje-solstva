import re
def vsota(niz):
    rx = re.compile(r'a(.*?),b')
    return re.findall(rx,niz)

def vsota2(a,b):
    return a+b

def vp(vsota2,a,b):
    return vsota2(a,b)*b