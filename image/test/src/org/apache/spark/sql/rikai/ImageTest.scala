package org.apache.spark.sql.rikai

import org.scalatest.FunSuite
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
import org.apache.spark.sql.rikai.Image


class ImageTest extends FunSuite with SparkTestSession {
  import spark.implicits._

  test("image udf") {
    val uri = "s3://path/to/image.png"
    val df = spark.sql(s"select image('${uri}') as image")
    val image = df.collect().head.get(0)
    assert(image == new Image("s3://path/to/image.png"))
    assert(image.toString === s"Image('${uri}')")
  }

  test("show image udt") {
    val df =
      Seq(
        (1, new Image("/tmp/image1.txt")),
        (2, new Image("/tmp/image2.txt"))
      ).toDF("id", "image")
    df.show()
  }
}
