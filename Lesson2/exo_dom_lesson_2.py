#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 23:13:37 2017
@author: olivier
Extraction (scrapping) des dépenses et investissement de la Commune de Paris en 
euros par habitants et selon la Moyenne de la strate
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

url = ('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom'
       '=056&dep=075&type=BPS&param=5&exercice=')
col = ['annee', 'Euros par habitant', 'Moyenne de la strate']

tot = ["TOTAL DES PRODUITS DE FONCTIONNEMENT", 
       "TOTAL DES CHARGES DE FONCTIONNEMENT",
       "TOTAL DES RESSOURCES D'INVESTISSEMENT"]


def get_i(soup, s):
    ''' Renvoie le numéro de la ligne du tableau ou se trouve le mot "string"
    '''
    il = [i for i in range(1, len(soup)) if soup[i].get_text().find(s) > -1]
    return il[0]

def get_j(soup, s):
    ''' Renvoie le numéro de la colonne du tableau ou se trouve le mot "string"
    '''
    i = get_i(soup, s)
    soup2 = soup[i].select("th")
    jl = [j for j in range(1, len(soup2)) if soup2[j].get_text().find(s) > -1]
    return jl[0]


''' Extraction des données
'''
M = []; # Matrice qui récupère les données
for annee in range (2010, 2016):
    res = requests.get(url + str(annee))
    soup = BeautifulSoup(res.text, 'html.parser').select("table")[2].select("tr")
    jl = [get_j(soup, string) for string in col[1:]]
    il = [get_i(soup, string) for string in tot]
    
    for i in il:
        val1 = int(soup[i].select("td")[jl[0]].get_text().replace(' ', ''))
        val2 = int(soup[i].select("td")[jl[1]].get_text().replace(' ', ''))
        M.append([annee, val1, val2])

''' Mise des données sous forme de DataFrame
'''
TP = pd.DataFrame(M[0::3][:], columns = col).set_index(['annee'])
TC = pd.DataFrame(M[1::3][:], columns = col).set_index(['annee'])
TR = pd.DataFrame(M[2::3][:], columns = col).set_index(['annee'])



''' Visualisation des données des dépenses et investissements en euros par 
habitants
'''
# Graphique
fig1 = plt.figure()
plt.plot(TP[col[1]], label=tot[0])
plt.plot(TC[col[1]], label=tot[1])
plt.plot(TR[col[1]], label=tot[2])
ax = fig1.add_subplot(111)
ax.set_title('Dépenses et investissements de la Commune de Paris')
legend = ax.legend(loc='center', shadow=True, fontsize='x-small')
ax.set_xlabel('Années')
ax.set_ylabel(col[1])
ax.grid()
plt.show()
