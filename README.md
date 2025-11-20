# 2I2D - Projet Maison

Ce projet correspond à la maquette d’une maison connectée / intelligente, réalisé dans le cadre de l’enseignement 2I2D (Ingénierie, Innovation & Développement Durable). Il utilise un Raspberry Pi Pico pour gérer des capteurs (température, luminosité, mouvement, etc.) et effectuer des actions/connecter des systèmes pour superviser l’environnement de la maison.


## 1. Contexte & objectif

Ce projet est un projet scolaire / pédagogique dans le cadre d’un projet de terminale STI2D spécialité 2I2D.

L’objectif principal est de créer une maquette domotique, avec des capteurs et des actionneurs, pour simuler un environnement “intelligent” :

- mesurer la température, la luminosité, le mouvement, etc.
- afficher ces données, les loguer, peut-être déclencher des actions selon des seuils.

Le Raspberry Pi Pico est utilisé comme “cerveau” du système, pour piloter les capteurs et récupérer les informations.

## 2. Fonctionnalités

Voici les fonctionnalités implémentées / prévues :

- Lecture de la température
- Mesure de la luminosité
- Détection de mouvement
- Affichage ou transmission des valeurs lues
- Log ou enregistrement des données

(Possiblement) déclenchement d’alertes ou d’actions selon des seuils (ex : si la luminosité < X, allumer une lampe)

Test/unité : des scripts de test sont fournis (```TempératureTest.py, TestLuminosité.py, MouvementTest.py```)

## 3. Architecture
### Matériels

- Raspberry Pi Pico
- Capteur de température (par exemple une sonde)
- Capteur de luminosité
- Capteur de mouvement (PIR, ou autre)

(Éventuellement) actionneurs (lampe, alarme, etc.)

### Logiciel

Le code principal est dans ```main.py```

Des scripts de test :

```MouvementTest.py```
```TempératureTest.py```
```TestLuminosité.py```

Utilisation de Python (MicroPython probable, étant donné le Pico)

Structure simple : lecture des capteurs, traitement / conditions, log ou action

## 4. Installation

Voici comment configurer le projet :

Cloner le dépôt :

```git clone https://github.com/Lumino-2-0/2I2D-Projet-Maison.git```
```cd 2I2D-Projet-Maison```

- Installer MicroPython sur le Raspberry Pi Pico (si ce n’est pas déjà fait) :
- Télécharger le firmware MicroPython pour le Pico
- Flasher le Pico avec l’outil approprié
- Copier les fichiers ```.py``` dans le Pico :
- Copier ```main.py```
- Copier les scripts de test
- Brancher les capteurs (température, luminosité, mouvement) aux broches correspondantes sur le Pico.

## 5. Utilisation

Allumer le Pico : il démarrera automatiquement ```main.py``` si bien configuré.

Les mesures de capteurs seront lues périodiquement.

Le code peut afficher les valeurs (via le port série) ou exécuter des actions selon des seuils.

## 6. Tests

```MouvementTest.py``` : vérifier que le capteur de mouvement fonctionne correctement.

```TempératureTest.py``` : lire la température et s’assurer que les valeurs sont raisonnables.

```TestLuminosité.py``` : mesurer la luminosité et vérifier les valeurs lues en conditions variables.

Ces tests peuvent être utilisés pour valider que le câblage matériel est correct avant d’intégrer les capteurs dans le main.py.
