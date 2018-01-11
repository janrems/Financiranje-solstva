import re
def vsota(niz):
    rx = re.compile('.*?<table class="wikitable sortable">'
                    '(.*)'
                    '</table>.*?')
    x = re.findall(rx,niz)
    return x

def vsota1(niz):
    rx = re.compile('a'
                    '(.*?)'
                    'b')
    x = re.findall(rx,niz)
    return x

def vsota2(niz):
    rx = re.compile(r'<'
                    r'(.*?)'
                    r'\\')
    x = re.findall(rx,niz)
    return x
x = [1,2,3,4]
for i in range (0,len(x)):
    print(x[i])


str= 'sda,sd'
l = str.split(',')
print(x)
for a in x:
    a = 1