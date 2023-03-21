# Projet-Robot-LU2IN013
https://github.com/baskiotisn/2IN013robot2022


main.py: fichier principal (initialisation de tout ce qu'il faut pour le fonctionnement du robot)


FICHIERS .IA (Fonctionnalité expérimentale)
Les fichiers textes ".ia" permettent de générer une instance de la classe IA à l'aide de la méthode openIA()

Syntaxe:
    -- Possibilité d'écrire des commentaires en commençant la ligne par // -- 

    --Instructions de base--
    avancer d=10 v=10 a=10; //Avance d'une distance d (cm), à une vitesse v (t/s), avec un angle a (pourcentage, de -100 à 100)

    tourner a=90 v=10; //Tourne sur place d'un angle a (degré), à une vitesse v (t/2)

    -- IA "complexes" --
    for(i){
        //Répète i fois l'IA
    }

    while(cond){
        //Effectue l'IA en boucle tant que la condition est vérifiée
    }

    if(cond){
        //IA 1
    }
    else{
        //IA 2
    } //A chaque step, avance dans l'IA 1 si la condition est vérifiée, dans l'IA 2 sinon

    -- Variables --
    a = 10 * 5 //Initialise une variable a, utilisable dans les conditions/print/definition des autres variables

    Il y a 2 variables spéciales:
        - capteur_distance : renvoie la valeur du capteur de distance
        - capteur_balise : renvoie la coordonnée x de la balise détectée par la caméra du robot

    -- Autres instructions --
    print(expr) //Affiche la valeur de l'expression dans la console


Pour un exemple concret, regarder le fichier test.ia