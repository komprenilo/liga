from liga.spark import init_session

spark = init_session(conf={"spark.port.maxRetries": 128}, jar_type="local")
