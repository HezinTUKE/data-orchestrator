# import os
#
# from pyspark.sql import SparkSession
#
# from application.config import get_config_section
#
# # os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
#
#
# spark = (
#     SparkSession.builder.appName("ReadDataFromS3")
#     .config(
#         "spark.jars.packages",
#         "org.apache.hadoop:hadoop-aws:3.4.0,com.amazonaws:aws-java-sdk-bundle:1.12.761",
#     )
#     .config(
#         "spark.hadoop.fs.s3a.aws.credentials.provider",
#         "com.amazonaws.auth.profile.ProfileCredentialsProvider",
#     )
#     .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
#     .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
#     .config("spark.hadoop.fs.s3a.connection.establish.timeout", "60000")
#     .config("spark.hadoop.fs.s3a.connection.request.timeout", "60000")
#     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
#     .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
#     .getOrCreate()
# )
#
# hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3a.connection.timeout", "60000")
# hadoop_conf.set("fs.s3a.connection.establish.timeout", "60000")
# hadoop_conf.set("fs.s3a.connection.request.timeout", "60000")
# hadoop_conf.set("fs.s3a.attempts.maximum", "10")
# hadoop_conf.set("fs.s3a.retry.limit", "10")
# hadoop_conf.set("fs.s3a.retry.interval", "500")
