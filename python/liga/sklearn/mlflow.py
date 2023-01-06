import rikai
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
                f"Clustering without predict method is not supported"
            )
    elif isinstance(model, TransformerMixin):
        return "liga.sklearn.models.transformer"
    else:
        raise RuntimeError(f"No corresponding ModelType yet")


def log_model(
    model: Any,
    registered_model_name: Optional[str] = None,
    schema: Optional[str] = None,
    customized_flavor: Optional[str] = "liga.sklearn.codegen",
    labels: Optional[dict] = None,
    artifact_path: str = "model",
    **kwargs: Any,
) -> None:
    model_type = _get_model_type(model)
    rikai.mlflow.sklearn.log_model(  # type: ignore[attr-defined]
        model,
        artifact_path,
        schema,
        registered_model_name,
        customized_flavor,
        model_type,
        labels,
        **kwargs,
    )
