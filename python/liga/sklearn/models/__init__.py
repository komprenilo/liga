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

"""
Base ModelType for sklearn
"""

from abc import ABC
from typing import Callable, Any

from liga.registry.model import ModelSpec, ModelType


class SklearnModelType(ModelType, ABC):
    """Base :py:class:`ModelType` for Sklearn"""

    def __init__(self) -> None:
        self.model: Any = None

    def load_model(self, spec: ModelSpec, **kwargs: Any) -> None:
        self.model = spec.load_model()

    def transform(self) -> Callable:
        # Do nothing in Sklearn
        pass
