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

from liga.mixin import Pretrained
from liga.exceptions import SpecError

from liga.registry.base import ModelSpec, Registry
from liga.registry.model import NOURI_SPEC_SCHEMA


__all__ = ["DummyModelSpec", "DummyRegistry"]


class DummyModelSpec(ModelSpec):
    def __init__(
        self,
        raw_spec: "ModelSpec",
        need_validate: bool = True,
    ):
        spec = {
            "version": "1.0",
            "options": raw_spec.get("options", {}),
            "schema": raw_spec.get("schema", None),
            "model": {
                "flavor": raw_spec.get("flavor", None),
                "type": raw_spec.get("modelType", None),
            },
        }
        if not spec["schema"]:
            del spec["schema"]
        super().__init__(
            spec, need_validate=need_validate, spec_schema=NOURI_SPEC_SCHEMA
        )

    def validate_spec_schema(self):
        super().validate_spec_schema()
        if not isinstance(self.model_type, Pretrained):
            raise SpecError(
                "ModelType with Pretrained mixin required if no URI is specified"  # noqa E501
            )

    def load_model(self):
        raise RuntimeError("DummyModelSpec does not load model")


class DummyRegistry(Registry):
    """Dummy Model Registry without URI"""

    def __repr__(self):
        return "DummyRegistry"

    def make_model_spec(self, raw_spec: dict):
        spec = DummyModelSpec(raw_spec)
        return spec
