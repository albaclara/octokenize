# -*-coding:Utf-8 -*
#multiTokenisingOc.py
#Eve Séguier
# 06/06/2018
# This program tokenizes all the files that are in the input repertory and puts the result in out repertory


#===============
# Environnement
#===============
import sys
import os 
import tokenizingOc

       
repficin = "../corpus_brut/"
repficout = "../corpus_seg/"
#os.remove("../corpus_seg/*.*")

os.makedirs(repficout, exist_ok=True)

for ficin in os.listdir(repficin):
    
    if os.path.isfile(repficin + ficin) : 
        print(ficin)
        tokenizingOc.tokenize(repficin+ficin, 1)
    	


