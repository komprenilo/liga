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

package net.xmacs.liga.spark.expressions

import org.apache.spark.sql.catalyst.FunctionIdentifier
import org.apache.spark.sql.catalyst.analysis.FunctionRegistry.FunctionBuilder
import org.apache.spark.sql.catalyst.expressions.ExpressionInfo

/** '''`ML_PREDICT`''' Expression in Spark SQL.
  *
  *  `ML_PREDICT` can be used in `SELECT / WHERE / ORDER BY` clauses. Its SQL syntax
  *  is defined as:
  *
  * {{{
  *   ML_PREDICT({ model_name | model_uri }, col [, col ...])
  * }}}
  */
object Predict {

  /** Function name in SQL query */
  val name = "ml_predict"

  val functionDescriptor
      : (FunctionIdentifier, ExpressionInfo, FunctionBuilder) = (
    new FunctionIdentifier(name),
    new ExpressionInfo("org.apache.spark.sql.ml.expressions", "Predict"),
    null
  )
}
