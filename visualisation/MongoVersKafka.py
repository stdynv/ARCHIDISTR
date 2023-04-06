from MongoDBConnecteur import MongoDBConnecteur
#from pyspark.sql import SparkSession
from kafka import KafkaProducer
import json
#from pymongo import MongoClient

class MongoDBVersKafka:
    def __init__(self, mongo_username, mongo_password, mongo_cluster, mongo_db_name, kafka_bootstrap_servers, kafka_topic_name):
        self.mongo_connector = MongoDBConnecteur
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic_name = kafka_topic_name

    def send_data_to_kafka(self, collection_name):
        # Récupérer les données de MongoDB
        data = self.mongo_connector.get_data(collection_name)

        # Créer un producteur Kafka
        producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        # Envoyer les données à Kafka
        for d in data:
            producer.send(self.kafka_topic_name, d)

        # Fermer le producteur Kafka
        producer.close()
