import pandas as pd
import requests
import re

from bs4 import BeautifulSoup

#==============================================================================
# Regular Expressions
#==============================================================================
re_tel = re.compile('(?:(?:\+|00)33|0)\s*([1-9])(?:[\s.-]*(\d{2}))'
                    '(?:[\s.-]*(\d{2}))(?:[\s.-]*(\d{2}))(?:[\s.-]*(\d{2}))')
re_url = re.compile('href="//(www\.leboncoin\.fr/voitures/\d{10}.[^"]{0,})"')
re_ver = re.compile('(INTENS|LIFE|ZEN)')
re_num = re.compile('(\d{1,2})?\s?(\d{3})|(\d{1,2})')
#==============================================================================
# Catégories des champs
#==============================================================================
region = ['ile_de_france', 'paca', 'aquitaine']
version = ['INTENS', 'LIFE', 'ZEN']
typeVend = {'pro': 'c', 'par': 'p'}
#==============================================================================
# Dataframe pour stocker résultats
#==============================================================================
df = pd.DataFrame(columns=['Région', 'Année-modèle', 'Kilométrage', 
                           'Prix', 'Vendeur', 'Téléphone', 'Version'])

urla = 'https://www.leboncoin.fr/voitures/offres/'
urlb ='&brd=Renault&mdl=Zoe&f='
#==============================================================================
# Récupérer valeurs des champs spécifique à la voiture vendue
#==============================================================================
def get_features(soup):
    row = {}
    feat = ['Année-modèle', 'Prix', 'Kilométrage']
    description = soup.find("p", class_='value')
    if description is not None:
        tel = re_tel.findall(description.text)
        version = re_ver.findall(description.text.upper())
        if len(tel) > 0:
            tel = tel[0]
            telClean = '0' + tel[0] + ' ' + ' '.join(tel[1:]);
            row['Téléphone'] = telClean
        if len(version)>0:
            row['Version'] = version[0]
        featureSoupList = soup.find_all('h2', class_='clearfix')
        for featureSoup in featureSoupList:
            f = featureSoup.find('span').text
            if f in feat:
                row[f] = featureSoup.find('span', class_="value").text.strip()
                row[f] = int(''.join(re_num.findall(row[f])[0]))   
    return row
#==============================================================================
# Former une nouvelle ligne avec tous les champs trouvés
#==============================================================================
def get_row(url):
    row = dict()
    row['Région'] = reg
    row['Vendeur'] = j
    res = requests.get('https://' + url)
    soup = BeautifulSoup(res.text, 'html.parser')
    row.update(get_features(soup))
    return row
#==============================================================================
# Boucle sur région, type vendeur et pages
#==============================================================================
for reg in region:
    for j in typeVend.keys():
        page = 0;
        while True:
            page = page + 1
            url1 = urla + reg + '/?o=' + str(page) + urlb + typeVend[j]
            res = requests.get(url1)
            soup = BeautifulSoup(res.text, 'html.parser')
            url_list = re_url.findall(str(soup))
            if len(url_list) == 0:
                break
            for url in url_list:
                df = df.append(get_row(url), ignore_index=True) 

df.shape
df_clean = df.dropna(axis=0)
df_clean.to_csv(path_or_buf='~/myGitHub/Olivier-Loison/Lesson4/RenaultZoe.csv')
#==============================================================================
# Argus lacentrale.fr
#==============================================================================
df_version_annee = df_clean[['Version', 'Année-modèle']].drop_duplicates()
ar = [];
classe = "jsRefinedQuot"
urla = "https://www.lacentrale.fr/cote-auto-renault-zoe-" 
for i in range(df_version_annee.shape[0]):
    url = urla + df_version_annee.iloc[i,0].lower() +"+charge+rapide-" + \
          str(df_version_annee.iloc[i,1]) + ".html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    ar.append(int(soup.find("span", class_=classe).text.replace(' ','')))
df_version_annee['argus'] = ar
#==============================================================================
# Merge + clean +  chèreté + last save
#==============================================================================
df_clea2 = pd.merge(df_clean, df_version_annee, 
                     on=['Année-modèle', 'Version'])
df_clea2['chere'] = df_clea2['argus'] < df_clea2['Prix']
df_clea2.sort_index
df_clea2.to_csv(path_or_buf='~/myGitHub/Olivier-Loison/Lesson4/RenaultZoe.csv')