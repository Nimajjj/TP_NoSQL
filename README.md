# Guide d'Installation et d'Utilisation du Replica Set MongoDB

## Préambule

Ce guide détaille le processus d'installation et de manipulation de MongoDB configuré en mode Replica Set à l'aide de Docker et de scripts Python. Suivez les instructions ci-dessous pour mettre en place l'environnement et exécuter les opérations nécessaires sur la base de données.

### Conditions Préalables

- Docker doit être installé sur votre système. Vous pouvez télécharger Docker [ici](https://docs.docker.com/get-docker/).
- Assurez-vous de posséder une copie de ce projet en exécutant la commande suivante :
  ```
  git clone https://github.com/Nimajjj/TP_NoSQL
  ```

## Configuration de l'Environnement MongoDB

### Mise en Route avec Docker Compose

Pour initialiser les instances MongoDB dans une configuration Replica Set, utilisez le fichier `docker-compose.yml` fourni. Lancez les instances en exécutant :

```bash
docker-compose up -d
```

Cette commande démarre trois conteneurs Docker configurés comme suit :

- **mongo1**
- **mongo2**
- **mongo3**

Pour vérifier le démarrage des instances et leur configuration, connectez-vous à l'une d'elles avec :

```bash
docker exec -it mongo1 bash
```

Changez `mongo1` par `mongo2` ou `mongo3` selon le conteneur auquel vous voulez accéder. Ensuite, accédez à MongoDB avec :

```bash
mongosh
```

Vérifiez le statut du Replica Set avec :

```bash
rs.status()
```

## Création de Données Factices

Les données fictives sont générées à l'aide du script `simulation_data.py`, situé dans le dossier `scripts`. Avant de le lancer, assurez-vous de transférer le script dans le conteneur `mongo1` :

```bash
docker cp ./scripts mongo1:/usr/src
```

Accédez à `mongo1` et installez Python et ses dépendances nécessaires :

```bash
apt-get update
apt-get install python3 python3-pip
pip3 install pymongo faker
```

Générez ensuite les données en exécutant :

```bash
cd /usr/src/scripts
python3 simulation_data.py
```

## Opérations via la CLI MongoDB

Pour insérer les données générées dans MongoDB, utilisez :

```bash
mongoimport --db db_cli --collection users --file ./data/generated_users.json --jsonArray
```

Pour manipuler ces données, utilisez la CLI `mongosh` en sélectionnant la base de données avec :

```bash
use db_cli
```

### Exemples de Commandes

- **Ajout d'un utilisateur** :
  ```bash
  db.users.insertOne({
      "name": "Alice Wonderland",
      "email": "alice@example.com",
      "age": 28,
      "createdAt": "2023-04-01T00:00:00"
  })
  ```
- **Trouver des utilisateurs de plus de 30 ans** :
  ```bash
  db.users.find({ "age": { $gt: 30 } })
  ```
- **Augmenter l'âge des utilisateurs de 5 ans** :
  ```bash
  db.users.updateMany({}, { $inc: { "age": 5 } })
  ```
- **Supprimer un utilisateur spécifique** :
  ```bash
  db.users.deleteOne({ "name": "Alice Wonderland" })
  ```

## Automatisation avec Python

Utilisez le script `database_manager.py` pour automatiser les opérations CRUD. Le script, déjà présent dans le conteneur, peut être exécuté avec :

```bash
python3 database_manager.py
```

## Récapitulatif des Différences CLI vs Python

L'automatisation avec Python permet une gestion d'erreur et une répétabilité des tâches qui ne sont pas possibles avec la CLI, offrant ainsi une approche plus robuste pour des manipulations fréquentes.

## Problèmes Rencontrés

Le principal défi a été la configuration initiale du Replica Set avec Docker Compose, qui nécessitait une compréhension détaillée des options de configuration de MongoDB. Des ajustements ont été faits pour simplifier l'installation et l'exécution des scripts Python directement dans les conteneurs.
