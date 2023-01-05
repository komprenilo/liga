from typing import List, Any
from rikai_sklearn.models import SklearnModelType


class Clustering(SklearnModelType):
    """Classification model type"""

    def schema(self) -> str:
        return "int"

    def predict(self, x: Any, *args: Any, **kwargs: Any) -> List[int]:
        assert self.model is not None
        return self.model.predict(x).tolist()

MODEL_TYPE=Clustering()
