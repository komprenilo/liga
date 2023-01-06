from typing import List, Any
from liga.sklearn.models import SklearnModelType


class Clustering(SklearnModelType):
    """Classification model type"""

    def schema(self) -> str:
        return "int"

    def predict(self, *args: Any, **kwargs: Any) -> List[int]:
        assert self.model is not None
        assert len(args) == 1
        return self.model.predict(args[0]).tolist()


MODEL_TYPE = Clustering()
