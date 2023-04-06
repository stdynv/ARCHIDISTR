# Projet architecture distribuée

## Introduction

### Membres de l'équipe :

- Hichem
- Yassine
- Lucas GAIO

### Outils

- Trello (gestion de projet) : https://trello.com/invite/b/EuYMDhT2/ATTI44375d96b82a0c5a0bcf8aca40e7dd88C6661CD2/architecture-distribuee 
- Github (répot) : https://github.com/Voldlov/architecture-distribuee.git 
- Python (langage)
- Docker
- Spark
- Kafka

## Consignes



## Notre sujet

### Travail préliminaire

Contexte métier, objectif et sources de données
Choisir les technologies 


## Utiliser les fichiers

Use docker compose to start the containers

`docker compose up -d`


The docker compose file create and use a spark master, two workers, one jupyter notebook with spark and one kafka container.
Additionally a zookeeper container is present as a kafka container, ignore that.

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

The correct command to start the script "spark_kafka.py" should be 

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 spark_kafka.py`

Still investigating the best way to use this.

### commande pour lancer le producer et consumer avec spark submit
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /workspace/KafkaProducer_spark.py & spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.0 /workspace/KafkaConsumer_spark.py

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /workspace/CryptoProducer.py & spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.0 /workspace/CryptoConsumer.py