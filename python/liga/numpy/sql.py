import numpy as np


def literal(arr: np.ndarray) -> str:
    assert len(arr.shape) == 1
    arr_str = ",".join([str(i) for i in arr.tolist()])
    return f"array({arr_str})"
