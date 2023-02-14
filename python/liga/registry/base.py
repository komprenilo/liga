#  Copyright 2021 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import importlib
from abc import ABC, abstractmethod
from typing import Any, Tuple
from types import ModuleType, FunctionType

from pyspark.serializers import CloudPickleSerializer
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType

from liga.internal.reflection import find_class
from liga.exceptions import SpecError
from liga.registry.model import ModelSpec, is_fully_qualified_name
from liga.logging import logger


__all__ = ["Registry"]


_pickler = CloudPickleSerializer()


class Registry(ABC):
    """Base class of a Model Registry"""

    @abstractmethod
    def make_model_spec(self, raw_spec: "ModelSpec") -> ModelSpec:
        """Make a ModelSpec from the raw model spec

        Parameters
        ----------
        spec : ModelSpec
        """

    def resolve(self, raw_spec: "ModelSpec") -> Tuple:
        """Resolve a model from the raw model spec.

        Parameters
        ----------
        spec : ModelSpec
        """
        name = raw_spec["name"]  # type: ignore[index]
        uri = raw_spec["uri"]  # type: ignore[index]
        logger.info("Resolving model %s from %s", name, uri)
        return udf_from_spec(self.make_model_spec(raw_spec))

    def resolve_schema(self, raw_spec: "ModelSpec") -> str:
        """Resolve the model schema from the raw model spec."""
        name = raw_spec["name"]  # type: ignore[index]
        uri = raw_spec["uri"]  # type: ignore[index]
        logger.info("Resolving schema of model %s from %s", name, uri)
        spec = self.make_model_spec(raw_spec)
        return spec.schema


def codegen_from_spec(spec: ModelSpec) -> ModuleType:
    """Resolve the codegen module from the model spec.

    Parameters
    ----------
    spec : ModelSpec

    Returns
    -------
    ModuleType
        The imported module for the specific flavor codegen
    """
    if is_fully_qualified_name(spec.flavor):
        codegen_module = f"{spec.flavor}.codegen"
    else:
        codegen_module = f"liga.{spec.flavor}.codegen"

    try:
        codegen = importlib.import_module(codegen_module)
        return codegen
    except ModuleNotFoundError:
        logger.error("Unsupported model flavor: %s", spec.flavor)
        raise


def schema_from_spec(registry_class: str, raw_spec: dict) -> str:
    cls = find_class(registry_class)
    registry = cls()
    return registry.resolve_schema(raw_spec)


def udf_from_spec(spec: ModelSpec) -> Tuple:
    """Return a UDF from a given ModelSpec

    Parameters
    ----------
    spec : ModelSpec
       Model spec payload

    Returns
    -------
    udt_ser_func, udf_func, udt_deser_func, returnType
        Spark UDF function name for the generated data.
    """
    if spec.version != "1.0":
        raise SpecError(
            f"Only spec version 1.0 is supported, got {spec.version}"
        )

    def deserialize_return(data: bytes) -> Any:
        return _pickler.loads(data)

    codegen = codegen_from_spec(spec)
    return (
        pickle_udt,
        codegen.generate_udf(spec),  # type: ignore[attr-defined]
        deserialize_return,
    )


def command_from_spec(registry_class: str, raw_spec: dict) -> Tuple:
    cls = find_class(registry_class)
    registry = cls()
    return registry.resolve(raw_spec)


@udf(returnType=BinaryType())
def pickle_udt(data: Any) -> None:
    return _pickler.dumps(data)


def unpickle_transform(data: bytes) -> Any:
    return _pickler.loads(data)
