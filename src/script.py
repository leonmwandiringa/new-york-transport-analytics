import sys
from pyspark.sql.window import Window
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.functions import split, round, weekofyear
from pyspark.sql.types import IntegerType
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.window import Window
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

# currently using raw spark, would have prefered using glue context
rides = spark.read.csv("s3://kubevisor-data/interviews/new-york/rides", header=True)
exchangeRates = spark.read.csv("s3://kubevisor-data/interviews/new-york/exchange-rates", header=True)

exchangedRidesDF = rides.withColumn("trip_date", split(f.col("lpep_pickup_datetime"), " ").getItem(0))
exchangedRidesDF = (exchangedRidesDF.join(exchangeRates, exchangedRidesDF.trip_date == exchangeRates.Date, "inner")
                        .drop("Date")
                        .withColumn("fare_amount", round((f.col("fare_amount").cast(IntegerType()) / f.col("USD")), 2))
                        .withColumn("tip_amount", round((f.col("tip_amount").cast(IntegerType()) / f.col("USD")), 2))
                        .withColumn("tolls_amount", round((f.col("tolls_amount").cast(IntegerType()) / f.col("USD")), 2))
                        .withColumn("total_amount", round((f.col("total_amount").cast(IntegerType()) / f.col("USD")), 2))
                        .withColumn("week", weekofyear(f.col("trip_date")))
                        .withColumn("total_week_amount", f.sum(f.col("total_amount").cast(IntegerType())).over(Window.partitionBy('week').orderBy().rowsBetween(-sys.maxsize, 0)))
                   )

weekWithHighestTotalAmount = exchangedRidesDF.agg({"total_week_amount": "max"}).collect()[0][0]
print(weekWithHighestTotalAmount)
exchangedRidesDF.filter(f.col("total_week_amount") == weekWithHighestTotalAmount).show()
