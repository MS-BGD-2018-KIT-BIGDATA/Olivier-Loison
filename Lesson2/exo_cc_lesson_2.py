#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:28:29 2017

@author: olivier
"""

import requests
from bs4 import BeautifulSoup

url = ("https://www.cdiscount.com/search/10/")

end_html = ".html#_his_'"

marques = ["acer", "dell"]

Nsoldes = [];
Ntot = [];
i = 0;
for m in marques:
    res = requests.get(url + m + end_html)
    soup = BeautifulSoup(res.text, 'html.parser')#.select("table")[2].select("tr")
    
    psoldes = soup.find_all(class_ = "prdtPrSt")
    ptot = soup.find_all(class_ = "price")
    Nsoldes.append(len(psoldes))
    Ntot.append(len(ptot))
    print("La marque " + m + " a " + str(Nsoldes[i]) + " produits soldés sur " + str(Ntot[i]) )
    print("soit un ratio de  " + str(float(Nsoldes[i])/Ntot[i]*100) + '%')
    i +=1;

