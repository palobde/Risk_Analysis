# -*- coding: utf-8 -*-
__author__ = 'Gilles Eric Zagre + Pascal Dan Trinh '

# IMPORTATIONS DE MODULES
import os
import sys  # <--- Pour recuperer les arguments entre en commande
import re
import math  # <--- Pour effectuer les calculs mathematiques (log10, sqrt...)
import operator  # <--- Module permettant de trier dictionnaires selon les valeur des entrees
import numpy as np
import datetime
from datetime import datetime, timedelta




# ******** Fonction de calcul de la VAR historique *********************************************************
def var_hist(pf_titres,titres_quant,T,seuil,database):
# Input:
#     - pf_titres: Liste contenant les titres du portefeuille
#     - titres_quant: Liste contenant ls quantites pour chaque titre
#     - T: Periode de la var (ex: Pour VAR hebdo T=5). Defaut=1 (var journaliere)
#     - seuil: seuil de la var en %(ex:95)
#     - database: Base de donnee (liste de liste) l'historique des prix de cloture de chaque titre.
#                 (ex: La permiere liste contient les prix de cloture du 1er titre de pf_titre)
#                Preter attention a la longueur des liste de prix de cloture (defaut=3 mois) 
# Output: 
#   [VAR, CVAR]: Liste contenant la VAR historique calculée et la VAR Conditionnelle
#
    VAR=0.0
    CVAR=0.0

    # Verifications mineures des donnees d'entrees
    if len(pf_titres) != len(titres_quant):
        print ("Erreur 1 sur les listes du pf")
        return 0
    if len(pf_titres) != len(database):
        print ("Erreur 1 sur la base de donnees")
        return 0
    if len(database[0]) != len(database[1]):
        print ("Erreur 2 sur la base de donnees")
        return 0
    if seuil>100.0 or seuil<0.0:
        print ("Erreur sur le seuil")
        return 0
    if T not in [1,5,20]:
        T=1
    # Verification de la valeur actuelle du portefeuille
    Value = sum(np.array(titres_quant)*np.array([x[0] for x in database]))
    print ('Valeur actuelle du portefeuille : ')
    print (Value)
    
    # Calcul de l'historique des rendements pour chaque titre   (liste de liste)
    titres_yield_list = []
    for titre_data in database:
        titre_yields = [(titre_data[i]-titre_data[i+T])/titre_data[i+T] for i in range(len(titre_data)-T)]
        titres_yield_list.append(titre_yields) 
    #print ('Rendements Titre 1',titres_yield_list)
    
    pf_titres_yhist=[]
    for timestep in range(len(titres_yield_list[1])): # Attention les rendements n'ont pas la mm taille que les prix de cloture
        pf_titres_ylist = [x[timestep] for x in titres_yield_list] 
        pf_titres_yhist.append(pf_titres_ylist)
    #print ('Rendements Titre 2',pf_titres_yhist)

    # Calcul de l'historique des rendements pour le portefeuille (liste)
    quant=np.array(titres_quant)
    pf_yield_hist = [sum(np.array(x)*quant) for x in pf_titres_yhist]
    print ('Rendements Portefeuille: ')
    print (pf_yield_hist)

    # Calcul de la VAR historique
    pf_yield_array = np.array(pf_yield_hist)
    VAR = np.percentile(pf_yield_array, (100-seuil))

    # Calcul de la VAR Conditionnelle

    return [VAR, CVAR]
        
# # Fonction de calcul de la VAR Monte-Carlo
# def var_mc(hist_yield,seuil): # 
    # VAR=0.0
    # if seuil>100.0 or seuil<0.0:
        # print ("Erreur sur le seuil")
        # return 0
    # else:
        # yield_array = np.array(hist_yield)
        # VAR = np.percentile(yield_array, seuil)
        # return VAR
        
# Fonction de calcul de la VAR Parametrique


# Exemple sur le portefeuille actuel de PolyFinances:  
pf_titres_PF = ['XIU.TO','CAM.TO','GIB-A.TO','PJC-A.TO','SLB','TEVA','FTS.TO','CNR.TO','SU.TO','TRI.TO','BCE.TO','POT.TO','VRX.TO','SAP.TO','BBD-B.TO']
titres_quant_PF = [0,246,91,166,0,15,115,54,116,86,84,110,9,127,607]
T=1
seuil=95
# Lecture sur base de donnees de YahooFinance (ou google)
from yahoo_finance import Share # ou from googlefinance import getQuotes
# Specifier les dates de debut (moins recent) et de fin (plus recent) de l'historique
start_hist = '2015-10-24'
end_hist = '2016-04-25'
# Base de donnees des prix de cloture
database_PF_0 = []
for titre in pf_titres_PF: # Pour chaque titre du portefeuille, 
    data = Share(titre).get_historical(start_hist, end_hist) # enregistrer l'historique , 
    daily_close_list=[float(dico['Close']) for dico in data] # convertir et mettre les prix de cloture dans une liste
    database_PF_0.append(daily_close_list) # Ajouter a la base de donnees
# Reduire la bd pour que chaque titre ait le mm nombre d'historique
long_hist = [len(x) for x in database_PF_0]
hist_max = min(long_hist)
database_PF=[x[0:hist_max] for x in database_PF_0]
#print database_PF 

# Calculons la VAR historique journaliere
VAR_H_PF_j =var_hist(pf_titres_PF,titres_quant_PF,T,seuil,database_PF)
print ('VAR historique jr PF : ' ,VAR_H_PF_j)
# Calculons la VAR historique hebdo
VAR_H_PF_h =var_hist(pf_titres_PF,titres_quant_PF,5,seuil,database_PF)
print ('VAR historique hebdo PF : ' ,VAR_H_PF_h)
# Calculons la VAR historique mensuelle
VAR_H_PF_m =var_hist(pf_titres_PF,titres_quant_PF,20,seuil,database_PF)
print ('VAR historique mensuelle PF : ' ,VAR_H_PF_m)








        