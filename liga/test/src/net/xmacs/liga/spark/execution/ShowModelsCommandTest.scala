/*
 * Copyright 2021 Rikai authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package net.xmacs.liga.spark.execution

import net.xmacs.liga.SparkTestSession
import net.xmacs.liga.model.{Model, ModelAlreadyExistException}
import org.scalatest.funsuite.AnyFunSuite

class ShowModelsCommandTest extends AnyFunSuite with SparkTestSession {

  import spark.implicits._

  test("show empty") {
    val expected =
      Seq
        .empty[(String, String, String, String)]
        .toDF("name", "flavor", "uri", "options")
    assertEqual(spark.sql("SHOW MODELS"), expected)
  }

  test("show models") {
    spark
      .sql(
        "CREATE MODEL model_foo LOCATION 'test://model/foo'"
      )

    val expected =
      Seq(("model_foo", "", "test://model/foo", "")).toDF(
        "name",
        "plugin",
        "uri",
        "options"
      )
    val result = spark.sql("SHOW MODELS")
    assertEqual(result, expected)
  }

  test("show models with options") {
    spark
      .sql(
        "CREATE MODEL model_options USING pytorch LOCATION 'test://foo' OPTIONS (foo='bar',num=1.2,flag=True)"
      )

    val expected_options = Seq(
      "foo" -> "bar",
      "num" -> "1.2",
      "flag" -> "true"
    ).toMap
    val expected = Seq(
      (
        "model_options",
        "pytorch",
        "test://foo",
        Model.serializeOptions(expected_options)
      )
    ).toDF("name", "plugin", "uri", "options")
    assertEqual(spark.sql("SHOW MODELS"), expected)
  }

  test("show multiple models") {
    spark
      .sql(
        "CREATE MODEL model_foo LOCATION 'test://foo' OPTIONS (foo='bar',num=1.2,flag=True)"
      )
    assert(spark.sql("SHOW MODELS").count() == 1)

    spark
      .sql(
        "CREATE MODEL model_bar LOCATION 'test://bar' OPTIONS (foo='bar',num=1.2,flag=True)"
      )
    assert(spark.sql("SHOW MODELS").count() == 2)

    // same name
    assertThrows[ModelAlreadyExistException] {
      spark.sql("CREATE MODEL model_foo LOCATION 'test://foo2'")
    }
    assert(spark.sql("SHOW MODELS").count() == 2)

    // drop model
    spark.sql("DROP MODEL model_foo")
    assert(spark.sql("SHOW MODELS").count() == 1)
  }
}
