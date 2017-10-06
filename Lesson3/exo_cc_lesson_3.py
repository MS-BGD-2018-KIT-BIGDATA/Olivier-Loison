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
import sys

from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool

""" les 100 plus grandes villes  de France"""
url = ("https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/")
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser').table.find_all('tr')[1:]
names = list(map(lambda s: s.text.split()[1], soup))




""" API """
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
payload = {
		'origins' : '|'.join(names),
		'destinations' : '|'.join(names), 
		'mode' : 'driving',
		#'api_key' : api_key
        }

r = requests.get(base_url, params = payload)
x = json.loads(r.text)
for isrc, src in enumerate(x['origin_addresses']):
				for idst, dst in enumerate(x['destination_addresses']):
					row = x['rows'][isrc]
                    for i in range(len(row)):
                        M.append(row['elements'][i]['distance']['value'])
                    
M2 = np.array(M)
M2.reshape(len(origins), len(origins))


