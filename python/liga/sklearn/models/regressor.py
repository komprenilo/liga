from typing import List, Any
from liga.sklearn.models import SklearnModelType


class Regressor(SklearnModelType):
    def schema(self) -> str:
        return "float"

    def predict(self, *args: Any, **kwargs: Any) -> List[float]:
        assert self.model is not None
        assert len(args) == 1
        return self.model.predict(args[0]).tolist()


MODEL_TYPE = Regressor()
