# -*-coding:Utf-8 -*
#tokenisingOc.py
#Eve Séguier
# 06/06/2018
# This program tokenizes file .txt (UTF8) and create file txt (UTF8) with one word by line
# tokenize(ficin,ficout,clean), with clean = 0/1
# if clean = 1 ==> cleaning(elem,elemBefore)
# this treatment remove proper names, numbers, punctuation, units of mesurement and  words which contain letters which are not in the occitan alphabet
# After treatment all words are in low case


#===============
# Environnement
#===============

import os.path
import re
#from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

#===================================
# Standardization of the punctuation
#===================================
def standardization(line) :
    line = line.replace("\r","")
    line =line.replace("`","'")
    line =line.replace("‘","'")
    line =line.replace("’","'")
    line =line.replace("‘","'")
    line =line.replace("'","'")
    line =line.replace(",",",")
    line =line.replace("­","-")
    line =line.replace("•","·")

    return line


#============================================
# Normalization - Insertion of \t for cutting
#============================================
def normalization(word) :
    #pb with word_tokenize which transforms characters
    word =word.replace("``",'"')
    word =word.replace("''",'"')
    word =word.replace("“",'"')
    word =word.replace("”",'"')


    wordWithTab = []   
    word = re.sub(r'(\w+)(\.)(\w+)',r'\1\t\2\t\3',word)     # to correct when there is no space after the full stop
    word = re.sub(r'(\w+)\*',r'\1',word)     # to correct when there is * after a word
    word = re.sub(r'(\w+)-(\w)-(\w+)',r'\1\t\2\t\3',word)     # - before and after like -n-,-z-,-t- etc.
    word = re.sub(r'(\w+)\-(zu|zo|me|te|li|lo|la|nos|vos|los|las|lor)$',r'\1\t\2',word)  # pronouns placed after
    word = re.sub(r'^([zZ])\-(\w+)',r'\1\t\2',word)   #z-
    word = re.sub(r'^([dlmnstDLMNST]s?\')(\w+)',r'\1\t\2',word)	#contraction with apostrophe like d' l' etc ... and pronoun ns'
    word = re.sub(r'(^\w+|^)([qnvQNV][us]\')(\w+)',r'\1\2\t\3',word) #qu' ...	 
    word = re.sub(r'(^[çcbzu]\')(\w+)',r'\1\t\2',word) 	

    # pronouns
    #word = re.sub(r'(\w+)\-(vos|ne|[st][eu]?'?|l[aoi']s?|me|d'|en|[nv]os|u)$',r'\1\t\2',word) 
    word = re.sub(r'(\w+)(\'[mnstuv]s?)$',r'\1\t\2',word) ; # pronouns gascons like 'm 't 'i 's 'u 'us 'n 'v 'ns 'vs...	
    word = re.sub(r'(\w+)(\'[mnstuv]s?)$',r'\1\t\2',word) ; # pronouns gascons like 'm 't 'i 's 'u 'us 'n 'v 'ns 'vs...	
    
    
	
    #cutting
    wordWithTab = word.split("\t"); 	
 
    return wordWithTab

#===================================
# Selection of real words
#===================================

def cleaning(word, wordBefore) :
    """
    Remove proper names, numbers, punctuation, units of mesurement and  words which contain letters which are not in the occitan alphabet
    After treatment all words are in low case
    """
    forbiddenwords = ["http","html","the","pdf"]
    word = word.strip('\n ')
    word = re.sub(r'^(\")?(\w+)(\"|\*)?',r'\2',word)     # word like "myword" , myword*
    
    with open("reject.txt", 'a', newline='', encoding='utf-8') as reject :

        # remove proper names, except when they are after punctuation   . ? !  
        if word in forbiddenwords :
             reject.write(word+"**** word forbidden "+"\n")
             word = "<FORBIDDEN WORD>"
        else :
            if  ( re.search(r"^[A-ZÁÉÍÓÚÀÈÒ]",word) ) and  ((re.search(r"^\w+",wordBefore) ) or ( wordBefore not in ['.','?','!',''])) :
                reject.write(word+"**** nom propre"+"\n")
                word = "<PROPER NAME>"


            else :
                 
                 # remove numbers and punctuation or words which contain letters which are not in the occitan alphabet

                 word = word.lower()             
                 if  not (re.search(r"^\'?([a-j]|[l-v]|x|z|à|á|ç|è|é|ë|í|ò|ó|ú|ü|·|\.|\?|\!)+((\s+|\-)([a-j]|[l-v]|x|z|à|á|ç|è|é|ë|í|ò|ó|ú|ü|·)+)*\'?$",word)) :
                     reject.write(word+","+wordBefore+"   **** nombre, ponctu, lettres hors alphabet"+"\n")
                     word = "<PUNCTUATION OR NUMBER OR NOT OCCITAN WORD>"
  

                 else :
                     # remove units of measurement
                     units = []
                     units = ['kg','hg','dg','cg','mg','k','cd','rad','sr','hz','j','w','n','pa','c','v','f','t','h','lm','lx','bq','gy','sv','cat','km','hm','dm','cm','mm']
                     if word in units :
                         reject.write(word+"**** mesure"+"\n")
                         word = "<UNITS OF MEASUREMENT>"


                 


    reject.close()
    return word

#===================================
# Main program
#===================================
def tokenize(stringinput,clean):

 
    #================================
    #Reading of the  line 
    #================================
    stringinput =stringinput.replace("\n"," ")
    wordslist = []
    elemBefore = ''
    line = stringinput
    line = line.strip('\n ')
    line = standardization(line) 
    #line = protectionNumber(line)
    #tokenization = word_tokenize(line)
    tokenization = nltk.word_tokenize(line)
    correctTokens = []
    listNotToWrite = []
    for elem in tokenization :
       correctTokens = correctTokens+normalization(elem)

    for elem in correctTokens : 
       if clean :
           elem = cleaning(elem,elemBefore)
           listNotToWrite += ['.','!','?','<PROPER NAME>','<PUNCTUATION OR NUMBER OR NOT OCCITAN WORD>','<UNITS OF MEASUREMENT>','<FORBIDDEN WORD>']
           
       if elem not in listNotToWrite :  
           wordslist.append(elem)   
       elemBefore = elem
    return wordslist




if __name__ == "__main__":

    stringinput = input("Input string : ")
    print(stringinput)
    mywords = tokenize(stringinput,1)
    print(mywords)
