from datetime import datetime, timedelta
from kafka import KafkaProducer
import snscrape.modules.twitter as sntwitter
import json
import time
import pandas as pd
from pyspark.sql import SparkSession
import findspark

findspark.init()

# Configuration de Kafka
bootstrap_servers = ['broker:29092']
topicName = 'tge'

# Configuration de la recherche Twitter
search_terms = ['#btc', '#XRP', '#eth','#DOT']
query = ' OR '.join(search_terms) + ' lang:en'
maxTweets = 10
timedate=datetime.now() + timedelta(seconds=30)

# Connexion au producteur Kafka
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Récupération des tweets avec snscrape et envoi au topic Kafka
for tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    print(tweet[1].date)
    if datetime.now() > timedate:
        break
    tweet_dict = {'Datetime': str(tweet[1].date), 'Tweet Id': str(tweet[1].id), 'text': tweet[1].content, 'Username': tweet[1].user.username}
    producer.send(topicName, value=tweet_dict)
    print(tweet_dict)
    print(datetime.now())
    time.sleep(1) # Pause de 1 seconde pour éviter de spammer l'API Twitter

    
producer.flush()