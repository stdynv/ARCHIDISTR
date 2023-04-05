import requests
import json
import datetime,time
from kafka import KafkaProducer

# Liste des cryptos à récupérer


# Configuration du Kafka Producer
producer = KafkaProducer(bootstrap_servers=['broker:29092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

crypto_list = ["bitcoin", "ethereum", "ripple"]
start_time = int(time.time())
# convert to timestamp 


while int(time.time()) < start_time + 200:
    for crypto in crypto_list:
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={crypto}"
        response = requests.get(url)
        data = response.json()[0]
        # print(data["current_price"])
        current_price = data["current_price"]
        date = datetime.datetime.now()
        message = {"crypto": crypto, "value": current_price, "date": date.strftime("%d-%m-%Y %H:%M:%S")}
        print(message)
        producer.send('crypto-values-f', value=message)
    # Récupération toutes les 5 minutes
    time.sleep(30)