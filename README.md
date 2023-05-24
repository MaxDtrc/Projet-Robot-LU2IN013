# Projet-Robot-LU2IN013
https://github.com/baskiotisn/2IN013robot2022

Documentation :
https://maxdtrc.github.io/Projet-Robot-LU2IN013/


main.py: fichier principal (initialisation de tout ce qu'il faut pour le fonctionnement du robot)


FICHIERS .IA
Les fichiers textes ".ia" permettent de générer une instance de la classe IA à l'aide de la méthode openIA()

Syntaxe:
    -- Possibilité d'écrire des commentaires en commençant la ligne par // -- 

    --Instructions de base--
    avancer d=10 v=10 a=10 //Avance d'une distance d (cm), à une vitesse v (t/s), avec un angle a (pourcentage, de -100 à 100)

    tourner a=90 v=10 //Tourne sur place d'un angle a (degré), à une vitesse v (t/s)

    tourner_tete a=90 //Tourne la tête du robot à un angle a (degré, entre 0 et 180)


    -- IA "complexes" --
    for(i){
        //Répète i fois l'IA
    }

    while(cond){
        //Effectue l'IA en boucle tant que la condition est vérifiée
    }

    alterner(cond){
        //IA 1
    }
    else{
        //IA 2
    } //A chaque step, avance dans l'IA 1 si la condition est vérifiée, dans l'IA 2 sinon

    if(cond){
        //IA 1
    }
    else{
        //IA 2
    } //Evalue la condition au début, puis réalise l'ia 1 ou l'ia 2 selon le résultat (le else n'est pas obligatoire)

    -- Variables --
    a = 10 * 5 //Initialise une variable a, utilisable dans les conditions/print/for/definition des autres variables

    Il y a 5 variables spéciales:
        - random : renvoie une valeur aléatoire entre 0 et 10000000
        - capteur_distance : renvoie la valeur du capteur de distance
        - capteur_balise : renvoie la coordonnée x de la balise (RJBV) détectée par la caméra du robot
        - type_balise : renvoie le type de la balise (BJ) détectée par le robot
        - pos_balise : renvoie la position de la balise (BJ) détectée par le robot

    Il est possible de rajouter des variables spéciales dans la classe Variables de controleur.py, méthode "substituerVariable" 

    -- Autres instructions --
    print(expr) //Affiche la valeur de l'expression dans la console


Pour un exemple concret, regarder le fichier test.ia
