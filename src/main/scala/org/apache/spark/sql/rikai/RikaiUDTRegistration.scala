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
package org.apache.spark.sql.rikai

import org.apache.spark.internal.Logging
import org.apache.spark.sql.types.{DataType, UserDefinedType}

import scala.collection.mutable

object RikaiUDTRegistration extends Serializable with Logging {
  private lazy val schemaMap: mutable.Map[String, DataType] = mutable.Map()

  def register(schemaName: String, dataType: DataType): Unit = {
    if (schemaMap.contains(schemaName)) {
      logWarning(
        s"Cannot register UDT for `${schemaName}`, which is already registered."
      )
    } else {
      schemaMap += ((schemaName, dataType))
    }
  }

  def exists(schemaName: String): Boolean = schemaMap.contains(schemaName)

  def getUDT(schemaName: String): Option[DataType] = {
    schemaMap.get(schemaName)
  }
}
