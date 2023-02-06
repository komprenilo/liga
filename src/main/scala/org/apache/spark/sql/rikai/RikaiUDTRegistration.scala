package org.apache.spark.sql.rikai

import org.apache.spark.internal.Logging
import org.apache.spark.sql.types.{DataType, UserDefinedType}

import scala.collection.mutable

object RikaiUDTRegistration extends Serializable with Logging {
  private lazy val schemaMap: mutable.Map[String, DataType] = mutable.Map()

  def register(schemaName: String, dataType: DataType): Unit = {
    if (schemaMap.contains(schemaName)) {
      logWarning(
        s"Cannot register UDT for ${schemaName}, which is already registered."
      )
    } else {
      // When register UDT with class name, we can't check if the UDT class is an UserDefinedType,
      // or not. The check is deferred.
      schemaMap += ((schemaName, dataType))
    }
  }

  def exists(schemaName: String): Boolean = schemaMap.contains(schemaName)

  /** Returns the Class of UserDefinedType for the name of a given user class.
    *
    * @param schemaName schema name of user class
    * @return Option value of the Class object of UserDefinedType
    */
  def getUDT(schemaName: String): Option[DataType] = {
    schemaMap.get(schemaName)
  }
}
