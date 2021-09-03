# octokenize
Tokenize strings or files in occitan

Entrée : fichiers texte brut (ou avec balises html) dans ./corpus_brut 

Sortie : fichiers tokenisés dans ./corpus_seg (en faire une sauvegarde ailleurs) et fichier reject.txt dans ./progTokenize qui liste les mots rejetés.

Vérifier que ./corpus_seg est vide avant le lancement du programme dans le répertoire ./progTokenize :

> python3 multiTokenizingOc.py   

Le programme fait appel à tokenizingOc.py qui exécute les traitements sur chaque fichier. Les fichiers en sortie s’appellent S_NomDuFichierEntrée.

La tokenisation s’effectue en plusieurs phases :

    • standardisation de la ponctuation
    • tokenisation avec word_tokenize de nltk.tokenize 
    • normalisation (en particulier traitement des pronoms gascons et de l’apostrophe en limousin)
    • nettoyage   ( le paramètre clean est à 1) : suppression des noms propres (s’il ne sont pas derrière . ? ! suivi d’un espace), des unités de mesure, des signes de ponctuations, des nombres, des mots contenant des caractères qui ne font pas partie de l’alphabet occitan, des mots de la liste des mots interdits (« pdf »  par exemple)
