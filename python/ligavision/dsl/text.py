#  Copyright 2021 Rikai Authors
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

from typing import Tuple

from ligavision.dsl.base import Drawable, Renderer
from ligavision.dsl import conf


class Text(Drawable):
    """Render a Text

    Parameters
    ----------
    text : str
        The text content to be rendered
    xy : Tuple[int, int]
        The location to render the text
    color : str, optional
        The RGB color string to render the text
    """

    def __init__(
            self,
            text: str,
            xy: Tuple[int, int],
            color: str = conf.text.color,
    ):
        self.text = text
        self.xy = xy
        self.color = color

    def _render(self, render: Renderer, **kwargs):
        kwargs["color"] = kwargs.get("color", self.color)
        return render.text(self.xy, self.text, **kwargs)
