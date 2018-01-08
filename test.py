import re
def vsota(niz):
    rx = re.compile('.*?<table class="wikitable sortable">'
                    '(.*)'
                    '</table>.*?')
    x = re.findall(rx,niz)
    return x

def vsota1(niz):
    rx = re.compile('a'
                    '(.*)'
                    'b')
    x = re.findall(rx,niz)
    return x

def vsota2(niz):
    rx = re.compile('a'
                    '(.*?)'
                    '"')
    x = re.findall(rx,niz)
    return x