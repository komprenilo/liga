#  Copyright 2023 Liga Authors
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
Utilities to log sklearn models to MLflow for Liga
"""

from typing import Any, Optional

from sklearn.base import (
    RegressorMixin,
    ClassifierMixin,
    TransformerMixin,
    ClusterMixin,
)


def _get_model_type(model: Any) -> str:
    if isinstance(model, RegressorMixin):
        return "liga.sklearn.models.regressor"
    elif isinstance(model, ClassifierMixin):
        return "liga.sklearn.models.classifier"
    elif isinstance(model, ClusterMixin):
        if "predict" in dir(model):
            return "liga.sklearn.models.cluster"
        else:
            raise RuntimeError(
                "Clustering without predict method is not supported"
            )
    elif isinstance(model, TransformerMixin):
        return "liga.sklearn.models.transformer"
    else:
        raise RuntimeError("No corresponding ModelType yet")


def log_model(
    model: Any,
    registered_model_name: Optional[str] = None,
    schema: Optional[str] = None,
    labels: Optional[dict] = None,
    **kwargs: Any,
) -> None:
    """
    Log sklearn models to MLflow with proper default settings
    """
    model_type = _get_model_type(model)

    from liga.mlflow import logger

    logger.sklearn.log_model(  # type: ignore[attr-defined]
        model,
        "model",
        schema,
        registered_model_name,
        "liga.sklearn",
        model_type,
        labels,
        **kwargs,
    )
