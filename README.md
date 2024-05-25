# Projet Rasa : Bot de Réservation de Restaurant

#### Ce projet implémente un chatbot capable de gérer des réservations pour un restaurant. Le bot peut effectuer plusieurs actions telles que la réservation de tables, la gestion des informations de réservation, et la fourniture de détails sur les allergènes et le menu du restaurant.

## Pré-requis
- ##### Python 3
- ##### Rasa
- ##### Un environnement virtuel Python

## Etapes pour démarrer le projet

#### 1. Cloner le dépôt du projet

#### 2. Créer et activer l'environnement virtuel
- `python3 -m venv venv`
- `source venv/bin/activate`

#### 3. Installer les dépendances

- `pip install rasa`

#### 4. Créer la base de données:

- `python3 create_databases.py`

#### 5. Entraîner le modèle Rasa:

- `rasa train`

## Lancer le bot Rasa

#### Dans un premier terminal:

#### 1. Déplacez-vous dans le répertoire du projet, activez l'environnement virtuel et lancer la conversation :

- `cd <nom_du_repertoire_du_projet>`
- `source venv/bin/activate`
- `rasa shell`

#### Ou pour plus de détails sur le débogage:

- `rasa shell --debug`

## Démarrer les actions personnalisées

#### Dans un second terminal:
#### 1. Déplacez-vous dans le répertoire du projet, activez l'environnement virtuel, puis exécutez les commandes suivantes :

- `cd <nom_du_repertoire_du_projet>`
- `source venv/bin/activate`
- `rasa run actions`

##### rasa run actions gère l'exécution de toutes les actions personnalisées définies dans votre projet Rasa. Ces actions personnalisées peuvent inclure des tâches telles que l'interaction avec des bases de données, l'envoi de requêtes à des API externes

## Interaction avec le bot sur une interface web avec Rasa x

#### Commandes à réaliser dans le projet chatbot-resto avec l'environnement python d'activé 

#### 1. Installer Rasa X :

##### Rasa X est une plateforme de développement de chatbots qui facilite la construction, l'entraînement, le déploiement et l'amélioration continue des assistants conversationnels basés sur Rasa.

- `pip install rasa-x`

#### 2. Démarrer Rasa X dans le navigateur :
- `rasa x`

#### 3. Déployer le Serveur Rasa :
- `rasa run -m models --enable-api --cors "*" --debug`
##### Cette commande démarre le serveur Rasa avec les options nécessaires pour activer l'API REST et permettre les requêtes CORS.

#### 4. Tester le Chat Widget

##### Tester le bot avec un chat widget dans une interface web (à executer dans un nouveau terminal dans le repertoire du projet et avec l'environnement python activé)

- `python3 -m http.server`
##### Ouvrez ensuite votre navigateur et accédez à l'URL http://localhost:8000/ pour visualiser et tester votre chat widget.

## Fonctionnalités du projet

#### Le bot développé permet de gérer plusieurs aspects des réservations de restaurant. Voici un aperçu des fonctionnalités disponibles :

#### 1. Réserver une table

- ##### Demande les informations nécessaires : date, nombre de personnes, nom et numéro de téléphone.
- ##### Vérifie la disponibilité de la table.
- ##### Génère un numéro de réservation unique.
- ##### Permet d'ajouter un commentaire à la réservation.

#### 2. Gérer les réservations

- ##### Annuler une réservation existante.
- ##### Afficher les informations d'une réservation et permettre la modification du commentaire.

#### 3. Informations supplémentaires

- ##### Fournit la liste des allergènes.
- ##### Donne le menu du jour.
- ##### Fournit un lien vers le menu complet du restaurant.

#### 4. Intégration du bot 

- #####  Sur une plateforme comme Slack pour une meilleure accessibilité




