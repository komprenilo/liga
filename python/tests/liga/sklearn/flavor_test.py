#  Copyright (c) 2022 Liga Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, StructField, StructType


def assert_sklearn_result(result):
    assert result.schema == StructType([StructField("pred", FloatType())])
    assert result.count() == 2


def test_customized_flaovr_via_logging(
    mlflow_tracking_uri: str, sklearn_lr_uri: str, spark: SparkSession
):
    model_name = "test_customized_flaovr_via_logging"

    spark.sql(
        f"""
        CREATE MODEL {model_name} LOCATION '{sklearn_lr_uri}';
        """
    )

    df = spark.range(2).selectExpr("id as x0", "id+1 as x1")
    df.createOrReplaceTempView("tbl_X")

    result = spark.sql(
        f"""
        select ML_PREDICT({model_name}, array(x0, x1)) as pred from tbl_X
        """
    )
    assert_sklearn_result(result)


def test_specified_flavor_via_sql(
    mlflow_tracking_uri: str, sklearn_lr_uri: str, spark: SparkSession
):
    df = spark.range(2).selectExpr("id as x0", "id+1 as x1")
    df.createOrReplaceTempView("tbl_X")

    model_name = "test_specified_flavor_via_sql"
    spark.sql(
        f"""
        CREATE MODEL {model_name} USING sklearn LOCATION '{sklearn_lr_uri}';
        """
    )
    spark.sql("show models").show()
    result = spark.sql(
        f"""
        select ML_PREDICT({model_name}, array(x0, x1)) as pred from tbl_X
        """
    )
    assert_sklearn_result(result)

    model_name = "test_full_qualified_flavor_via_sql"
    spark.sql(
        f"""
        CREATE MODEL {model_name} USING liga.sklearn LOCATION '{sklearn_lr_uri}';
        """
    )
    spark.sql("show models").show()
    result = spark.sql(
        f"""
        select ML_PREDICT({model_name}, array(x0, x1)) as pred from tbl_X
        """
    )
    assert_sklearn_result(result)

    model_name = "test_full_qualified_flavor_and_model_type"
    spark.sql(
        f"""
        CREATE MODEL {model_name}
        USING liga.sklearn
        FOR regressor
        LOCATION '{sklearn_lr_uri}';
        """
    )
    spark.sql("show models").show()
    result = spark.sql(
        f"""
        select ML_PREDICT({model_name}, array(x0, x1)) as pred from tbl_X
        """
    )
    assert_sklearn_result(result)
