# Projet architecture distribuée

## Introduction

### Membres de l'équipe :

- Hichem
- Yassine
- Lucas GAIO

### Outils

- Trello (gestion de projet) : https://trello.com/invite/b/EuYMDhT2/ATTI44375d96b82a0c5a0bcf8aca40e7dd88C6661CD2/architecture-distribuee 
- Github (dépôt) : https://github.com/Voldlov/architecture-distribuee.git 
- Langage : Python
- Contenneur : Docker
- Architecture distribuée et streaming : Spark & kafka
- Visualisation : Grafana

## Notre sujet

Nous sommes des futurs Data Engineer, dans le cadre de la fin du module "Architecture distribuée", lors de notre première année de Master chez Paris Ynov campus nous avons décidé de prendre comme sujet les cryptomonaies par rapport aux twittes. 

Notre objectif est de voir et comprendre l'impacte de ce réseau social sur la valeur des diverses monaies. 

## Utiliser les fichiers

### Lancer docker

Utiliser la commande suivante pour lancer le Docker File (il est normalement lancé avec le Docker Compose, donc inutile de le faire)

`docker build -t archi_distribuee ./docker `

Utiliser la commande suivante pour lancer le Docker Compose, le "-d" permet de le lancer en fond.

`docker-compose -f ./docker/docker-compose.yml up -d`

Le fichier Docker Compose créer et utilise un Master Spark, deux workers, un jupyer notebook avec des contenneurs spark et kafka. Il y a aussi présent Zookeeper. 

### Kafka

To test if kafka container and service is running, use these two commands in two differents terminals:

Producer
`docker exec --interactive --tty broker \                                                
kafka-console-producer --bootstrap-server broker:9092 \
--topic quickstart`

Consumer `docker exec --interactive --tty broker \
kafka-console-consumer --bootstrap-server broker:9092 \
--topic quickstart \
--from-beginning
`

This will create a producer and a consumer on the topic 'quickstart'. Whatever one or more producer on this topic is sending will be received by the consumer.

You can then test the python script "streamToKafkaProducerExample.py" locally, or wherever you want as long as this can access your localhost and its ports.

It should produce four time the message "Nouveaux messages" into the topic "Quickstart"

### Spark/Kafka

La commande pour démarrer le script "spark_kafka.py"

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 spark_kafka.py`

### Grafana / mongoDB

Accéder à Grafana :

`http://localhost:3001/login`

- login : "admin"
- mot de passe : "admin"

Lien vers mongoDB : mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/?retryWrites=true&w=majority 

pour installer le plugin mongodb à grafana (plus d'actualité) :

1. utiliser le dossier dans visualisation portant le nom "mongodb-grafana".
2. le mettre dans le fihcier plugins de grafana avec cette commande : `docker cp mongodb-grafana 9f6c6b7a71d2:/var/lib/grafana/plugins`