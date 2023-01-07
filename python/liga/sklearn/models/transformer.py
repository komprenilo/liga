#  Copyright 2022 Rikai Authors
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
ModelType: DimensionalityReduction
"""

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
