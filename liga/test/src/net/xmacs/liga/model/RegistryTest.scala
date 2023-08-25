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

package net.xmacs.liga.model

import net.xmacs.liga.model.testing.TestRegistry
import org.scalatest.BeforeAndAfter
import org.scalatest.funsuite.AnyFunSuite

class RegistryTest extends AnyFunSuite with BeforeAndAfter {

  before {
    Register.reset
    Registry.registerAll(
      Map(
        Registry.REGISTRY_IMPL_PREFIX + "test.impl" -> "net.xmacs.rikai.sql.model.testing.TestRegistry",
        Registry.DEFAULT_URI_ROOT_KEY -> "test:/"
      )
    )
  }

  after {
    Registry.reset
  }

  test("Resolve default uri") {
    val registry = Registry.getRegistry(Some("/tmp/foo/bar"))
    assert(registry.isInstanceOf[TestRegistry])
    val uri = Registry.normalize_uri("/tmp/foo/bar")
    val expected = "test:/tmp/foo/bar"
    assert(uri.toString == expected)
  }
}
