from __future__ import annotations

from abc import ABC
from typing import Callable, Any

from rikai.spark.sql.model import ModelSpec, ModelType


class SklearnModelType(ModelType, ABC):
    """Base :py:class:`ModelType` for Sklearn"""

    def __init__(self) -> None:
        self.model: Any = None

    def load_model(self, spec: ModelSpec, **kwargs: Any) -> None:
        self.model = spec.load_model()

    def transform(self) -> Callable:
        # Do nothing in Sklearn
        pass
