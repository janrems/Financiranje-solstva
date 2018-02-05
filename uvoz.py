import requests
import re
import os
import csv
import sys

url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={}'
#url glavne spletne strani

def url_v_niz(url):
    #Funkcija za argument dobi url "url" spletne strani in vrne njeno html kodo kot niz.
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Neuspela povezava na stran" + url)
        return
    # continue with the non-exceptional code
    if r.status_code == requests.codes.ok:
        return r.text
    print("Neuspel prenos strani" + url)
    return

def shrani_niz_v_datoteko(niz,mapa,ime):
    #"niz" zapiše v datoteko "ime", ki se  nahaja v mapi "mapa". Če je potrbno mapo ustvari. Če je "mapa" prazen niz, uporabi datoteko v kateri se nahajamo.
    os.makedirs(mapa,exist_ok = True)
    pot = os.path.join(mapa,ime)
    with open (pot,'w',encoding='utf-8') as datoteka:
        datoteka.write(niz)
    return None

def uvoz(url,mapa,ime):
    #Združi funkcji "url_v_niz" in "shrani_nize_v_datoteko" ter shrani 100 strani knjig
    for i in range(1,100):
        niz = url_v_niz(url.format(i))
        shrani_niz_v_datoteko(niz,mapa,ime.format(i))

    return None



def preberi_datoteko_kot_niz(mapa, ime):
    #Vrne vsebino "mapa"/"ime" kot niz
    pot = os.path.join(mapa, ime)
    with open(pot, 'r',encoding='utf-8') as datoteka:
        return datoteka.read()



def linki_knjige(mapa,ime):
    #Vrne seznam urljev spletnih strani posameznih knjig
    rx_link_knjige = re.compile('<a class="bookTitle" itemprop="url" href="'
                                '(.*?)'
                                '">',
                                re.DOTALL)
    seznam_seznamov = []
    for i in range(1,100):
        niz = preberi_datoteko_kot_niz(mapa, ime.format(i))
        seznam_url = re.findall(rx_link_knjige,niz)
        seznam_seznamov.append(seznam_url)
    seznam_linkov_knjige = []
    for l in seznam_seznamov:
        for item in l:
           seznam_linkov_knjige.append(item)
    return seznam_linkov_knjige

def linki_avtorji(mapa,ime):
    #Vrne seznam urljev spletnih strani posameznih knjig
    rx_link_avtor = re.compile('<a class="authorName" itemprop="url" href="'
                                '(.*?)'
                                '">',
                                re.DOTALL)
    seznam_seznamov = []
    for i in range(1,100):
        niz = preberi_datoteko_kot_niz(mapa, ime.format(i))
        seznam_url = re.findall(rx_link_avtor,niz)
        seznam_seznamov.append(seznam_url)
    seznam_linkov_avtor = []
    for l in seznam_seznamov:
        for item in l:
           seznam_linkov_avtor.append(item)
    return seznam_linkov_avtor


def poberi_strani_knjig():
    seznam = linki_knjige('Podatki','Stran_{}')
    url = 'https://www.goodreads.com{}'
    for i in range(1472,len(seznam)):
        niz = url_v_niz(url.format(seznam[i]))
        shrani_niz_v_datoteko(niz,'Podatki/Knjige','Knjiga_{}'.format(i+1))
    return None

def poberi_strani_avtorjev():
    seznam = linki_avtorji('Podatki','Stran_{}')
    for i in range(0,3228):
        niz = url_v_niz(seznam[i])
        shrani_niz_v_datoteko(niz,'Podatki/Avtorji','Avtor_{}'.format(i+1))
    return None




rx_podatki_knjige = re.compile(r'googletag\.pubads\(\)\.setTargeting\("shelf", '
                               r'(?P<zvrsti>.*?)\).*?'
                               r'<span class="item" style="display:none"><span class="fn">'
                               r'(?P<naslov>.*?)'
                               r'( \(.*?(?P<del_serije>.*?)\))?'
                               r'<'
                               r'.*?ratingValue">'
                               r'(?P<ocena>.*?)'
                               r'<.*?'
                               r'ratingCount" content="'
                               r'(?P<st_ocen>.*?)'
                               r'".*?'
                               r'class="uitext darkGreyText">.*?'
                               r'numberOfPages">'
                               r'(?P<st_strani>\d*?)'
                               r' .*?<.*?'
                               r'<div class="row">'
                               r'.*?(?P<leto_izdaje>\d{4}).*?'
                               r'(<nobr class="greyText">.*?)?'
                               r'((?P<leto_izida>\d{4}).*?)?'
                               r'<.*?',
                               re.DOTALL)


def podatki_knjige(mapa,ime):
    niz = preberi_datoteko_kot_niz(mapa,ime)
    ujemanje = rx_podatki_knjige.search(niz)
    if ujemanje:
        knjiga = ujemanje.groupdict()
        return knjiga
    else:
        print('error')


rx_podatki_avtor = re.compile(r'<h1 class="authorName">.*?>'
                              r'(?P<avtor>.*?)<'
                              r'(.*?<div class="dataTitle">Born</div>.*?\s*(?P<poreklo_avtorja>.*?)\s\s\s)?'
                              r'(.*?birthDate.*?(?P<leto_rojstva>\d{4}).*?<)?',
                              re.DOTALL)

def podatki_avtorja(mapa,ime):
    niz = preberi_datoteko_kot_niz(mapa,ime)
    ujemanje = rx_podatki_avtor.search(niz)
    if ujemanje:
        avtor = ujemanje.groupdict()
        return avtor
    else:
        print('error')

def uredi_podatke(mapa_knjiga,mapa_avtor,ime_knjige,ime_avtorja):
    knjiga = podatki_knjige(mapa_knjiga,ime_knjige)
    if knjiga['leto_izida'] == None:
        knjiga['leto_izida'] = knjiga['leto_izdaje']
    knjiga['ocena'] = float(knjiga['ocena'])
    knjiga['st_strani'] = int(knjiga['st_strani'])
    knjiga['st_ocen'] = int(knjiga['st_ocen'])
    knjiga['leto_izdaje'] = int(knjiga['leto_izdaje'])
    knjiga['leto_izida'] = int(knjiga['leto_izida'])
    if knjiga['del_serije'] != None:
        if knjiga['del_serije'].replace(' ','') != knjiga['del_serije']:
            ujemanje = re.search(r'(.*)(,|\s)(\#(\d+))?',knjiga['del_serije'])
            if ujemanje.group(4) == None:
                knjiga['del_serije'] = ujemanje.group(4)
            else:
                knjiga['del_serije'] = int(ujemanje.group(4))
            knjiga['serija'] = re.sub(r',','',ujemanje.group(1))
    knjiga["zvrsti"] = knjiga["zvrsti"].strip('[]')
    knjiga["zvrsti"] = knjiga["zvrsti"].split(',')
    zvrsti = []
    for zvrst in knjiga["zvrsti"]:
        zvrst= zvrst.strip('"')
        zvrsti.append(zvrst)
    knjiga["zvrsti"] = zvrsti
    avtor = podatki_avtorja(mapa_avtor,ime_avtorja)
    if avtor['poreklo_avtorja'] != None:
        avtor['poreklo_avtorja'] = avtor['poreklo_avtorja'].split(',')
        avtor['poreklo_avtorja'] = avtor['poreklo_avtorja'][-1][1:]
    if avtor['leto_rojstva']!= None:
        if avtor['leto_rojstva'][0] != '0':
            avtor['leto_rojstva'] = int(avtor['leto_rojstva'])
        else:
            avtor['leto_rojstva'] = - int(avtor['leto_rojstva'])
    knjiga.update(avtor)
    return knjiga


def vrni_slovarje():
    seznam_slovarjev  = []
    for i in range(1,1201):
        slovar = uredi_podatke('Podatki/Knjige','Podatki/Avtorji','Knjiga_{}'.format(i),'Avtor_{}'.format(i))
        slovar['knjiga'] = i
        seznam_slovarjev.append(slovar)
        print(i)
    return seznam_slovarjev

def slovar_zanrov():
    sez = vrni_slovarje()
    sez_zvrsti = []
    for knjiga in sez:
        for zvrst in knjiga['zvrsti']:
            slovar = {'knjiga': knjiga['knjiga'], 'zvrst' : zvrst}
            sez_zvrsti.append(slovar)
    return sez_zvrsti




polja = ['leto_izdaje','leto_rojstva','zvrsti','avtor','knjiga','leto_izida','ocena','st_ocen','naslov', 'del_serije', 'st_strani','serija','poreklo_avtorja']
def zapisi_csv_knjige(polja, ime_datoteke):
    podatki = vrni_slovarje()
    with open(ime_datoteke, 'w',encoding='utf-8') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)


def zapisi_csv_zanri(polja, ime_datoteke):
    podatki = slovar_zanrov()
    with open(ime_datoteke, 'w',encoding='utf-8') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

