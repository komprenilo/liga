#  Copyright (c) 2023 Liga Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Convert numpy data into SQL literals
"""

import numpy as np


def literal(arr: np.ndarray) -> str:
    """
    Convert a Numpy Array to SQL literal
    """
    assert len(arr.shape) == 1
    arr_str = ",".join([str(i) for i in arr.tolist()])
    return f"array({arr_str})"
