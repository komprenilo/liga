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
import net.xmacs.liga.model.{Catalog, ModelAlreadyExistException}
import org.scalatest.funsuite.AnyFunSuite

class CreateModelCommandTest extends AnyFunSuite with SparkTestSession {

  test("create model from uri") {

    spark
      .sql(
        "CREATE MODEL model_created LOCATION 'test://model/created/from/uri'"
      )
      .count()
    assert(Catalog.testing.modelExists("model_created"))

    val model = Catalog.testing.getModel("model_created", spark).get
    assert(model.name == "model_created")
    assert(model.spec_uri == "test://model/created/from/uri")
    assert(model.options.isEmpty)
  }

  test("create model with options") {
    spark
      .sql(
        "CREATE MODEL qualified_opt " +
          "LOCATION 'test://foo/options' " +
          "OPTIONS (rikai.foo.bar=1.23, foo='bar', num=-1.23, batch=10, flag=True)"
      )
      .count()
    val model = Catalog.testing.getModel("qualified_opt", spark).get
    assert(
      model.options == Seq(
        "foo" -> "bar",
        "num" -> "-1.23",
        "flag" -> "true",
        "batch" -> "10",
        "rikai.foo.bar" -> "1.23"
      ).toMap
    )
  }

  test("model already exist") {
    spark.sql(
      "CREATE MODEL model_created LOCATION 'test://model/created/from/uri'"
    )
    assertThrows[ModelAlreadyExistException] {
      spark.sql("CREATE MODEL model_created LOCATION 'test://model/other/uri'")
    }
  }

  test("create model if not exists") {
    spark.sql(
      "CREATE MODEL model_created LOCATION 'test://model/created/from/uri'"
    )
    spark.sql(
      """
        |CREATE MODEL IF NOT EXISTS model_created
        |LOCATION 'test://model/created/from/uri'
        |""".stripMargin
    )
  }

  test("create or replace model") {
    spark.sql(
      "CREATE OR REPLACE MODEL replace_model LOCATION 'test://model/to_be_replaced'"
    )
    val to_be_replaced = Catalog.testing.getModel("replace_model", spark).get
    assert(to_be_replaced.spec_uri == "test://model/to_be_replaced")
    spark.sql(
      "CREATE OR REPLACE MODEL replace_model LOCATION 'test://model/replaced'"
    )
    val replaced = Catalog.testing.getModel("replace_model", spark).get
    assert(replaced.spec_uri == "test://model/replaced")
  }

  test("model plugin") {
    spark.sql(
      "CREATE MODEL tfmodel " +
        "USING tensorflow " +
        "LOCATION 'test://model/tfmodel'"
    )
    val model = Catalog.testing.getModel("tfmodel", spark).get
    assert(model.plugin.isDefined)
    assert(model.plugin.contains("tensorflow"))
  }
}
