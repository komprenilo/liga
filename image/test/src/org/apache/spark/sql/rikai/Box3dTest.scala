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

package org.apache.spark.sql.rikai

import org.apache.spark.sql.SaveMode
import org.scalatest.FunSuite

import java.io.File
import java.nio.file.Files
import scala.reflect.io.Directory


class Box3dTest extends FunSuite with SparkTestSession {
  import spark.implicits._

  test("test serialize 3d bounding box") {
    val testDir =
      new File(Files.createTempDirectory("rikai").toFile(), "dataset")

    val df = Seq(
      (1, new Box3d(new Point(1, 2, 3), 1, 2, 3, 2.7)),
      (
        2,
        new Box3d(
          new Point(2.5, 4.5, 6.5),
          1.2,
          2.3,
          3.4,
          2.3
        )
      )
    ).toDF("id", "b3")

    df.write.mode(SaveMode.Overwrite).format("parquet").save(testDir.toString())

    val actualDf = spark.read.format("parquet").load(testDir.toString())
    assert(df.count() == actualDf.count())
    assert(df.exceptAll(actualDf).isEmpty)

    new Directory(testDir).deleteRecursively()
  }

  test("show box udt") {
    val box1 = new Box3d(new Point(1, 2, 3), 1, 2, 3, 2.7)
    val box2 = new Box3d(new Point(2.5, 4.5, 6.5), 1.2, 2.3, 3.4, 2.3)
    val df = Seq((box1, 1), (box2, 2)).toDF("b3", "id")
    df.show()
  }
}
