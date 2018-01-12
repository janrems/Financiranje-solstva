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

nz= re.search(r'(^[A-Za-z]$)|((.*)(,|\s)(\#(\d+))?)','Harry')
k = re.search(r'.*','abc dsf,sd,')
r'(.*)(,|\s)\#(\d+)'
s = re.sub(r'(d)$','','abc dsf,sdl')

re.compile('googletag\.pubads\(\)\.setTargeting\("shelf", '
                               '(?P<zvrst>.*?)\).*?'
                               '<span class="item" style="display:none"><span class="fn">'
                               '(?P<naslov>.*?)'
                               '( \(.*?(?P<del_serije>.*?)\))?'
                               '<'
                               '.*?ratingValue">'
                               '(?P<ocena>.*?)'
                               '<.*?'
                               'ratingCount" content="'
                               '(?P<st_ocen>.*?)'
                               '".*?'
                               'class="uitext darkGreyText">.*?'
                               '(numberOfPages">?'
                               '(?P<st_strani>\d*?)?'
                               ' .*?<.*?'
                               '<div class="row">'
                               '.*?(?P<leto_izdaje>\d{4}).*?'
                               '(<nobr class="greyText">.*?)?'
                               '((?P<leto_izida>\d{4}).*?)?'
                               '<.*?'
                               '(<div class="infoBoxRowItem" itemprop=\'inLanguage\'>(?P<jezik_izdaje>.*?))?'
                               '<.*?',
                               re.DOTALL)
