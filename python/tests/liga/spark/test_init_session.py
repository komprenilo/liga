import pytest
import pyspark

from liga.spark import init_session, init_dbr_session


def test_init_session_with_empty_conf():
    pytest.skip()
    spark = init_session(conf={}, jar_type="local")
    spark.sql("show models").show()
    spark.stop()


def test_init_session_with_none_conf():
    pytest.skip()
    spark = init_session(jar_type="local")
    spark.sql("show models").show()
    spark.stop()


def test_init_session_with_no_jars():
    spark = init_dbr_session()
    with pytest.raises(
        pyspark.sql.utils.ParseException,
        match=r"missing 'FUNCTIONS'.*",
    ):
        spark.sql("show models").show()
    spark.stop()
