#  Copyright 2020 Rikai Authors
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

"""Mixins
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Mapping, Optional, Union

# Third Party
import numpy as np

__all__ = [
    "Asset",
    "Displayable",
    "Drawable",
    "ToDict",
]


def uri_equal(uri1: str, uri2: str) -> bool:
    """Return True if two URIs are equal."""
    if uri1 == uri2:
        return True
    from urllib.parse import urlparse
    parsed1 = urlparse(uri1)
    parsed2 = urlparse(uri2)
    if parsed1.scheme in ["", "file"] and parsed2.scheme in ["", "file"]:
        return (
                parsed1.netloc == parsed2.netloc and parsed1.path == parsed2.path
        )
    return False

class ToNumpy(ABC):
    """ToNumpy Mixin."""

    @abstractmethod
    def to_numpy(self) -> np.ndarray:
        """Returns the content as a numpy ndarray."""


class ToPIL(ABC):
    """ToPIL Mixin."""

    @abstractmethod
    def to_pil(self) -> "PIL.Image.Image":
        pass


class ToDict(ABC):
    """ToDict Mixin"""

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Displayable(ABC):
    """Mixin for notebook viz"""

    @abstractmethod
    def display(self, **kwargs) -> "IPython.display.DisplayObject":
        """Return an IPython.display.DisplayObject"""


class Drawable(ABC):
    """Mixin for a class that is drawable"""

    @abstractmethod
    def _render(self, render: "ligavision.dsl.Renderer", **kwargs) -> None:
        """Render the object using render."""

    def __matmul__(self, style: Union[dict, "ligavision.dsl.Style"]) -> Drawable:
        from ligavision.dsl import Style

        if not isinstance(style, (Mapping, Style)):
            raise ValueError(
                f"Must decorate drawable with a dict or style object"
                " but got {style}"
            )
        if isinstance(style, dict):
            style = Style(**style)
        return style(self)


class Asset(ABC):
    """cloud asset Mixin.
    Rikai uses asset to store certain blob on the cloud storage, to facilitate
    the functionality like fast query, example inspections, and etc.
    An asset is also a cell in a DataFrame for analytics. It offers both fast
    query on columnar format and easy tooling to access the actual data.
    Attributes
    ----------
    data : bytes, optional
        Embedded data
    uri : str
        URI of the external storage.
    """

    def __init__(
        self, data: Optional[bytes] = None, uri: Union[str, Path] = None
    ) -> None:
        assert (data is None) ^ (uri is None)
        assert data is None or isinstance(
            data, (bytes, bytearray)
        ), f"Expect bytes got {type(data)}"
        assert uri is None or isinstance(
            uri, (str, Path)
        ), f"Expect str/Path for uri, got {type(uri)}"
        self.data = data
        self.uri = str(uri) if uri is not None else None

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Asset) and uri_equal(self.uri, o.uri)

    @property
    def is_embedded(self) -> bool:
        """Returns True if this Asset has embedded data."""
        return self.data is not None

    def open(self, mode="rb") -> BinaryIO:
        """Open the asset and returned as random-accessible file object."""
        if self.is_embedded:
            return BytesIO(self.data)
        import fsspec
        return fsspec.open(self.uri, mode).open()
