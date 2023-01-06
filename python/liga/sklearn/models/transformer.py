from typing import List, Any
from liga.sklearn.models import SklearnModelType


class DimensionalityReduction(SklearnModelType):
    """Dimensionality reduction models.

    - PCA
    """

    def schema(self) -> str:
        return "array<float>"

    def predict(self, *args: Any, **kwargs: Any) -> List[float]:
        assert self.model is not None
        assert len(args) == 1
        return self.model.transform(args[0]).tolist()


MODEL_TYPE = DimensionalityReduction()
