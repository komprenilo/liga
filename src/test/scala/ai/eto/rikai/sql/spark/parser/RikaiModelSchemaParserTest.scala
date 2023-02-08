package ai.eto.rikai.sql.spark.parser

import ai.eto.rikai.SparkTestSession
import org.apache.spark.sql.rikai.NDArrayType
import org.apache.spark.sql.types.{ArrayType, BooleanType, IntegerType, StructField, StructType}
import org.scalatest.funsuite.AnyFunSuite

class RikaiModelSchemaParserTest extends AnyFunSuite with SparkTestSession {
  import ai.eto.rikai.sql.spark.parser.ModelSchemaParser.parse_schema

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
