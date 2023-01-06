from rikai.spark.utils import get_default_jar_version


def init_spark_session(conf=None, app_name="rikai", rikai_version=None):
    from pyspark.sql import SparkSession
    import os
    import sys
    
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    if not rikai_version:
        rikai_version = get_default_jar_version(use_snapshot=True)
    builder = (
        SparkSession.builder.appName(app_name)
        .config(
            "spark.jars.packages",
            ",".join(
                [
                    "ai.eto:rikai_2.12:{}".format(rikai_version),
                ]
            ),
        )
        .config(
            "spark.sql.extensions",
            "ai.eto.rikai.sql.spark.RikaiSparkSessionExtensions",
        )
        .config(
            "spark.driver.extraJavaOptions",
            "-Dio.netty.tryReflectionSetAccessible=true",
        )
        .config(
            "spark.executor.extraJavaOptions",
            "-Dio.netty.tryReflectionSetAccessible=true",
        )
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
    )
    conf = conf or {}
    for k, v in conf.items():
        builder = builder.config(k, v)
    session = builder.master("local[2]").getOrCreate()
    return session


spark = init_spark_session()