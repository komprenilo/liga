/*
 * Copyright 2023 Liga authors
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

package net.xmacs.rikai.sql.spark.parser

import net.xmacs.rikai.SparkTestSession
import org.apache.spark.sql.rikai.NDArrayType
import org.apache.spark.sql.types.{ArrayType, BooleanType, IntegerType, StructField, StructType}
import org.scalatest.funsuite.AnyFunSuite

class RikaiModelSchemaParserTest extends AnyFunSuite with SparkTestSession {
  import ModelSchemaParser.parse_schema

  test("test") {
    assert {
      parse_schema("bool") === BooleanType
    }
    assert {
      parse_schema("struct<a:bool, b:int>") ===
        StructType(Seq(StructField("a", BooleanType, true), StructField("b", IntegerType, true)))
    }
    assert {
      parse_schema("STRUCT<a:bool, b:int>") ===
        StructType(Seq(StructField("a", BooleanType, true), StructField("b", IntegerType, true)))
    }
    assert {
      parse_schema("array<int>") ===
        ArrayType(IntegerType, true)
    }
    assert {
      parse_schema("ARRAY<int>") ===
        ArrayType(IntegerType, true)
    }
    assert {
      parse_schema("ndarray") === NDArrayType
    }
    assert {
      parse_schema("array<ndarray>") === ArrayType(NDArrayType, true)
    }
  }
}
