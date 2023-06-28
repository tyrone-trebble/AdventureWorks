# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Change Date Format

# COMMAND ----------

from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_utc_timestamp, date_format, when
from pyspark.sql.types import TimestampType
import os

table_name = []

for i in dbutils.fs.ls('mnt/bronze/dbo/'):
    table_name.append(i.name.split('/')[0])

for i in table_name:
    path = '/mnt/bronze/dbo/' + i + '/'
    df = spark.read.format('parquet').load(path)
    column = df.columns
    
    for col in column:
     if "Date" in col or "date" in col:
         df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()),"UTC"), "yyyy-MM-dd"))
         
    output_path = '/mnt/silver/dbo/' + i + '/'
    df.write.format('delta').mode("overwrite").save(output_path)
