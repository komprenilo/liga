from typing import List, Any
from liga.sklearn.models import SklearnModelType


class Regressor(SklearnModelType):
    def schema(self) -> str:
        return "float"

    def predict(self, x: Any, *args: Any, **kwargs: Any) -> List[float]:
        assert self.model is not None
        return self.model.predict(x).tolist()


MODEL_TYPE = Regressor()
