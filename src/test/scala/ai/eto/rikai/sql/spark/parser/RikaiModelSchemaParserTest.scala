package ai.eto.rikai.sql.spark.parser

import ai.eto.rikai.SparkTestSession
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.apache.spark.sql.types.DataType
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
    println(parse_schema("bool").json)
    println(parse_schema("struct<a:bool, b:int>").json)
    println(parse_schema("STRUCT<a:bool, b:int>").json)
    println(parse_schema("array<int>").json)
    println(parse_schema("ARRAY<int>").json)
    println(parse_schema("ndarray").json)
  }
}
