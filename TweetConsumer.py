from pymongo import MongoClient
import re
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PASSWORD = os.getenv("MONGODB_ATLAS_PASSWORD")
MONGODB_ATLAS_URI = "mongodb+srv://{}:{}@cluster0.6jprsq1.mongodb.net/".format(MONGODB_ATLAS_USER, MONGODB_ATLAS_PASSWORD)

# Initialisation de SparkSession
spark = SparkSession.builder.appName("Test1")\
    .config("spark.jars.packages", "org.apach.spark:spark-sql-kafka-0-10_2.12:3.1.1")\
    .config("spark.jars.packages", "org.apach.spark:mongo-spark-connector_2.12:3.0.0")\
    .master("spark://spark-master:7077")\
    .config("spark.mongodb.input.uri", MONGODB_ATLAS_URI)\
    .config("spark.mongodb.output.uri", MONGODB_ATLAS_URI)\
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0")\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Configuration de Kafka
bootstrap_servers = ['broker:29092']
topicName = 'final'

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
    StructField("Datetime", StringType(), True),
    StructField("Tweet Id", StringType(), True),
    StructField("Username", StringType(), True),
    StructField("text", StringType(), True)])

# Connexion à MongoDB Atlas
client = MongoClient("mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db = client["Archi_distri"]
collection = db["Tweets"]

# Traitement des tweets
def process_tweet(tweet):
    text = tweet['text']
    # Clean the tweet content and extract text
    clean_tweet = re.sub(r'http\S+', '', text)  # Remove URLs
    clean_tweet = re.sub(r'@\S+', '', clean_tweet)  # Remove mentions
    clean_tweet = re.sub(r'RT\s+', '', clean_tweet)  # Remove retweets
    clean_tweet = re.sub(r'&[a-z]+;', '', clean_tweet)  # Remove HTML entities
    clean_tweet = re.sub(r'\n', ' ', clean_tweet)  # Replace newlines with spaces
    clean_tweet = re.sub(r'\s+', ' ', clean_tweet)  # Remove extra spaces
    tweet['Text_traité'] = clean_tweet.strip()  # Remove leading/trailing spaces
    print(tweet['Text_traité'])

# Transformation des données en DataFrame structuré
df_tweets = df.select(from_json(col("value").cast("string"), schema).alias("tweet"))

# Traitement des tweets et écriture dans MongoDB
query = df_tweets.writeStream \
    .foreach(process_tweet) \
    .option("forceDeleteTempCheckpointLocation", "true")\
    .option('spark.mongodb.connection.uri', 'MONGODB CONNECTION HERE')\
    .option('spark.mongodb.database', 'archi_distri')\
    .option('spark.mongodb.collection', 'tweets')\
    .option("checkpointLocation", "checkpoint") \
    .outputMode("append") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.format("mongo").mode("append").option("uri", "mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/Archi_distri.Tweets").save()) \
    .start()

query.awaitTermination()

query = df_tweets.writeStream \
    .foreach(process_tweet)\
    .format("console") \
    .start()

query.awaitTermination()
