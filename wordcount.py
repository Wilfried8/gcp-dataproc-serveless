import sys
from operator import add

from pyspark.sql import SparkSession
from datetime import datetime

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <input gcs file location> <output gcs location>", file=sys.stderr)
        sys.exit(-1)

    input_location = sys.argv[1]
    output_location = sys.argv[2]

    spark = SparkSession \
        .builder \
        .appName("PythonWordCount") \
        .getOrCreate()

    lines = spark.read.text(input_location).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(add)

    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    #counts.saveAsTextFile(f"{output_location}/{formatted_timestamp}/")
    counts.saveAsTextFile(output_location)
    spark.stop()