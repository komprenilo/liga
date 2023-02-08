package ai.eto.rikai.sql.spark.parser

import ai.eto.rikai.SparkTestSession
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.apache.spark.sql.rikai.NDArrayType
import org.apache.spark.sql.types.{ArrayType, BooleanType, DataType, IntegerType, StructField, StructType}
import org.scalatest.funsuite.AnyFunSuite

class RikaiModelSchemaParserTest extends AnyFunSuite with SparkTestSession {
  def parse_schema(schema: String): DataType = {
    val lexer = new RikaiModelSchemaLexer(
      new UpperCaseCharStream(CharStreams.fromString(schema))
    )
    val tokens = new CommonTokenStream(lexer)
    val parser = new RikaiModelSchemaParser(tokens)
    val visitor = new SparkDataTypeVisitor
    visitor.visitSchema(parser.schema())
  }

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
