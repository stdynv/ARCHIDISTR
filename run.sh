cd /opt/workspace &&

pip install -r requirements &&

#nohup python twitter_producer.py & &&
#nohup python coingecko_producer.py & &&

spark-submit spark_main_WIP.py