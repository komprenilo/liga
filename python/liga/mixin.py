#  Copyright 2020 Rikai Authors
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

"""Mixins
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

# Third Party
import numpy as np


__all__ = [
    "ToNumpy",
    "Pretrained",
]


class ToNumpy(ABC):
    """ToNumpy Mixin."""

    @abstractmethod
    def to_numpy(self) -> np.ndarray:
        """Returns the content as a numpy ndarray."""


class Pretrained(ABC):
    """Mixin for pretrained model"""

    @abstractmethod
    def pretrained_model(self) -> Any:
        pass
