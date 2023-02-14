#  Copyright 2022 Rikai Authors
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

import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, TypeVar, List

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from liga.internal.reflection import find_func
from liga.exceptions import SpecError
from liga.logging import logger

__all__ = ["ModelSpec", "ModelType"]


M = TypeVar("M")  # Model Type


# JSON schema specification for the model payload specifications
# used to validate model spec input
def gen_schema_spec(required_cols: List) -> dict:
    return {
        "type": "object",
        "properties": {
            "version": {
                "type": "string",
                "description": "Model SPEC format version",
            },
            "schema": {"type": "string"},
            "name": {"type": "string", "description": "Model name"},
            "model": {
                "type": "object",
                "description": "model description",
                "properties": {
                    "uri": {"type": "string"},
                    "flavor": {"type": "string"},
                    "type": {"type": "string"},
                },
                "required": required_cols,
            },
        },
        "required": ["version", "model"],
    }


SPEC_PAYLOAD_SCHEMA = gen_schema_spec(["uri"])
NOURI_SPEC_SCHEMA = gen_schema_spec(["flavor", "type"])


def is_fully_qualified_name(name: str) -> bool:
    return "." in name


def parse_model_type(flavor: str, model_type: str) -> "ModelType":
    model_modules_candidates = []

    if is_fully_qualified_name(model_type):
        model_modules_candidates.append(model_type)
    elif is_fully_qualified_name(flavor):
        model_modules_candidates.extend(
            [
                f"{flavor}.models.{model_type}",
            ]
        )
    else:
        model_modules_candidates.extend(
            [
                f"liga.{flavor}.models.{model_type}",
            ]
        )
    for model_module in model_modules_candidates:
        try:
            return find_func(f"{model_module}.MODEL_TYPE")
        except ModuleNotFoundError:
            pass
    raise ModuleNotFoundError(
        f"Model type not found for flavor/model_type: {flavor}/{model_type}"
    )


class ModelSpec(ABC):
    """Model Spec Payload

    Parameters
    ----------
    spec : dict
        Dictionary representation of an input spec
    need_validate : bool, default True.
        Validate the spec during construction. Default ``True``.
    """

    def __init__(
        self,
        spec: Dict[str, Any],
        need_validate: bool = True,
        spec_schema: dict = SPEC_PAYLOAD_SCHEMA,
    ) -> None:
        self._spec = spec
        self._spec["options"] = self._spec.get("options", {})
        self._spec_schema = spec_schema
        if need_validate:
            self.validate()

    def validate(self) -> None:
        """Validate model spec

        Raises
        ------
        SpecError
            If the spec is not well-formatted.
        """
        logger.debug("Validating spec: %s", self._spec)
        try:
            validate(instance=self._spec, schema=self._spec_schema)
        except ValidationError as e:
            raise SpecError(e.message) from e
        if not self.flavor or not self.model_type:
            raise SpecError("Missing model flavor or model type")

    @property
    def version(self) -> str:
        """Returns spec version."""
        return str(self._spec["version"])

    @property
    def name(self) -> str:
        """Return model name"""
        return self._spec["name"]

    @property
    def model_uri(self) -> str:
        """Return Model artifact URI"""
        return self._spec["model"]["uri"]

    @property
    def model_type(self) -> "ModelType":
        """Return model type"""
        mtype = self._spec["model"].get("type", None)
        if mtype:
            return parse_model_type(self.flavor, mtype)
        else:
            raise SpecError("ModelType is not available in spec")

    @abstractmethod
    def load_model(self) -> Any:
        """Load the model artifact specified in this spec"""

    def load_label_fn(self) -> Optional[Callable]:
        """Load the function that maps label id to human-readable string"""
        if "labels" in self._spec:
            uri = self._spec["labels"].get("uri")
            if uri:
                with open(uri) as f:
                    data = json.load(f)
                return lambda label_id: data[label_id]
            func = self._spec["labels"].get("func")
            if func:
                return find_func(func)
        return None

    @property
    def flavor(self) -> str:
        """Model flavor"""
        return self._spec["model"].get("flavor", "")

    @property
    def schema(self) -> str:
        """Return the output schema of the model."""
        if "schema" in self._spec:
            return self._spec["schema"]
        return self.model_type.schema()

    @property
    def options(self) -> Dict[str, Any]:
        """Model options"""
        return self._spec["options"]


class ModelType(ABC):
    """Base-class for a Model Type.

    A Model Type defines the functionalities which is required to run
    an arbitrary ML models in SQL ML, including:

    - Result schema: :py:meth:`schema`.
    - :py:meth:`transform`, pre-processing routine.
    - :py:meth:`predict`, inference **AND** post-processing routine.
    """

    @abstractmethod
    def load_model(self, spec: ModelSpec, **kwargs: Any) -> None:
        """Lazy loading the model from a :class:`ModelSpec`."""
        pass

    @abstractmethod
    def schema(self) -> str:
        """Return the string value of model schema.

        Examples
        --------

        >>> model_type.schema()
        ... "array<struct<box:box2d, score:float, label_id:int>>"
        """
        pass

    @abstractmethod
    def transform(self) -> Callable:
        """A callable to pre-process the data before calling inference.

        It will be feed into :py:class:`torch.data.DataLoader` or
        :py:meth:`tensorflow.data.Dataset.map`.

        """
        pass

    @abstractmethod
    def predict(self, *args: Any, **kwargs: Any) -> Any:
        """Run model inference and convert return types into
        Rikai-compatible types.

        """
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.predict(*args, **kwargs)

    def release(self) -> None:
        """Release underneath resources if applicable.

        It will be called after a model runner finishes a partition in Spark.
        """
        # Noop by default
        pass
