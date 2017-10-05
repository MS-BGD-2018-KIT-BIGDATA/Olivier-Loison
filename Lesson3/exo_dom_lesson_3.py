#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:28:29 2017
Rq ?100perpage pour être sur de tout charger
@author: olivier
"""


import getpass
import json
import numpy as np
import requests

from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


""" Identification pour l'API GitHub """
user = input('user :')
mpass = getpass.getpass('password: ')

""" Obtention de la liste des contributeurs dans une liste 'names' """
url = ("https://gist.github.com/paulmillr/2657075")
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser').table.find_all('tr')[1:]
names = list(map(lambda s: s.text.split()[1], soup))


""" Utilisation de l'API pour extraire et calculer la moyenne des stars """
url_d = "https://api.github.com/users/"
url_f = "/repos"

# fonction pour obtenir un array du nombre de stars par repro et pour 
# 1 contributeur
fun_stars = np.vectorize(lambda repo: repo['stargazers_count'])

# fonction pour obtenir un array indiquant si le contributeur est à la source 
# du repro (pas un fork)
fun_owner = np.vectorize(lambda repo: repo['fork'] == False)

# fonction pour obtenir la moyenne des stars pour chaque contributeur 
def fun_meanstars(name):
    r = requests.get(url_d + name + url_f, auth=HTTPBasicAuth(user, mpass))
    repoList = json.loads(r.text)
    return fun_stars(repoList)[fun_owner(repoList)].mean()

# dictionnaire pseudo/moyenne des stars
stars = dict((name,fun_meanstars(name)) for name in names[:20])

""" Print """
print('pseudo'.center(20) + '|' + 'AVG(stars)'.center(20) + '\n' + '_'*41)
for name in stars.keys():
    print(name.center(20) + '|' + ('%.1f' % stars[name]).center(20))    
