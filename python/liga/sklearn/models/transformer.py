from typing import List, Any
from rikai_sklearn.models import SklearnModelType

class DimensionalityReduction(SklearnModelType):
    """Dimensionality reduction models.

    - PCA
    """

    def schema(self) -> str:
        return "array<float>"

    def predict(self, x: Any, *args: Any, **kwargs: Any) -> List[float]:
        return self.model.transform(x).tolist()

MODEL_TYPE=DimensionalityReduction()
