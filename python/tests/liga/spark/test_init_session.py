import pytest
import py4j
import pyspark

from liga.spark import init_session

def test_init_session():
    spark = init_session(conf={"spark.jars":None})
    with pytest.raises(
        pyspark.sql.utils.ParseException,
        match=r"missing 'FUNCTIONS'.*",
    ):
        spark.sql("show models").show()


