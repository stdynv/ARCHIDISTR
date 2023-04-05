from pymongo import MongoClient
import re
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PASSWORD = os.getenv("MONGODB_ATLAS_PASSWORD")
MONGODB_ATLAS_URI = "mongodb+srv://{}:{}@cluster0.6jprsq1.mongodb.net/".format(MONGODB_ATLAS_USER, MONGODB_ATLAS_PASSWORD)

# Initialisation de SparkSession
spark = SparkSession.builder.appName("Test1")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")\
    .master("spark://spark-master:7077")\
    .config("spark.mongodb.input.uri", MONGODB_ATLAS_URI)\
    .config("spark.mongodb.output.uri", MONGODB_ATLAS_URI)\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Configuration de Kafka
bootstrap_servers = ['broker:29092']
topicName = 'crypto-values-f'

# Configuration du consommateur Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", topicName) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false")\
    .load()

# Définition du schéma pour le DataFrame
schema = StructType([
    StructField("crypto", StringType(), True),
    StructField("date", StringType(), True),
    StructField("valeur", DoubleType(), True)
])

# Connexion à MongoDB Atlas
client = MongoClient("mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/?retryWrites=true&w=majority")
db = client["Archi_dist"]
collection = db["crypto_collection"]


# Transformation des données en DataFrame structuré
df_cryptos = df.select(from_json(col("value").cast("string"), schema).alias("crypto"))

# Traitement des tweets et écriture dans MongoDB
query = df_cryptos.writeStream \
    .option("checkpointLocation", "checkpoint") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.format("mongo").mode("append").option("uri", "mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/Archi_dist.crypto_collection").save()) \
    .start()

query.awaitTermination()
