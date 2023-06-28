# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Changing column name

# COMMAND ----------

from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType
import os

table_name = []

#Iterate through silver container to assing to table array
for i in dbutils.fs.ls('mnt/silver/dbo/'):
    table_name.append(i.name.split('/')[0])

#Load delata files to data frame
for name in table_name:
    path = '/mnt/silver/dbo/' + name
    df = spark.read.format('delta').load(path)
 
    #Get the list of column names
    column_names = df.columns
    
    for old_col_name in column_names:
        #Convert column name from ColumnName to Column_Name format
         new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i - 1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")
         
         #Change the column name using withColumnRenamed and regexp_replace
         df = df.withColumnRenamed(old_col_name, new_col_name)
         
    output_path = '/mnt/gold/dbo/' + name + '/'
    df.write.format('delta').mode("overwrite").save(output_path)
