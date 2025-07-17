from application.spark.base import SparkSingleton

_spark_singleton = SparkSingleton()
spark = _spark_singleton.get_spark_instance()
