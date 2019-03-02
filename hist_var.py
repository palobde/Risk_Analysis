__author__ = 'ZGE'

# IMPORTATIONS DE MODULES
import os
import sys  # <--- Pour recuperer les arguments entre en commande
import re
import math  # <--- Pour effectuer les calculs mathematiques (log10, sqrt...)
import operator  # <--- Module permettant de trier dictionnaires selon les valeur des entrees
import numpy as np

from yahoo_finance import Share


# Fonction de calcul de la VAR historique
def calculVAR(hist_yield,seuil): # 
    VAR=0.0
    if seuil>100.0 or seuil<0.0:
        print ("Erreur sur le seuil")
        return 0
    else:
        yield_array = np.array(hist_yield)
        VAR = np.percentile(yield_array, seuil)
        return VAR
    
# Fonction qui calcule le rendement d'un portefeuille de titres
# def calculYield(titres)
        
# Exemple simple     
a = calculVAR([4, 5, 8, 24, 24, 45, 1, 0, 23],95) 
print a   

# Lecture sur base de donnees de YahooFinance
bombardier = Share('BBD-B.TO')
print bombardier.get_price()

from pprint import pprint
pprint(bombardier.get_historical('2015-12-28', '2016-01-25'))


# Lecture sur base de donnees de googlefinance
from googlefinance import getQuotes



#date_object = datetime.strptime('2016-04-18','%Y-%m-%d')
#date_object2 = date_object - timedelta(days=+1)
        