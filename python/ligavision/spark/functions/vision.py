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

"""Vision related Spark UDFs.
"""

# Standard library
from pathlib import Path
from typing import List, Union

# Third Party
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType

# Liga
from liga.numpy import ndarray
from ligavision.spark.types import Box2d, Image, ImageType

__all__ = [
    "crop",
    "to_image",
    "numpy_to_image",
]


@udf(returnType=ImageType())
def to_image(image_data: Union[bytes, bytearray, str, Path]) -> Image:
    """Build an :py:class:`Image` from
    bytes, file-like object, str, or :py:class:`~pathlib.Path`.

    Parameters
    ----------
    image_data : bytes, bytearray, str, Path
        The resource identifier or bytes of the source image.

    Return
    ------
    img: Image
        An Image from the given embedded data or URI

    Example
    -------

    >>> df = spark.read.format("image").load("<path-to-data>")
    >>>
    >>> df.withColumn("new_image", to_image("image.data"))
    """
    return Image(image_data)


@udf(returnType=ImageType())
def numpy_to_image(
    array: ndarray, uri: str, format: str = None, **kwargs
) -> Image:
    """Convert a numpy array to image, and upload to external storage.

    Parameters
    ----------
    array : :py:class:`numpy.ndarray`
        Image data.
    uri : str
        The base directory to copy the image to.
    format : str, optional
        The image format to save as. See
        `supported formats <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save>`_ for details.
    kwargs : dict, optional
        Optional arguments to pass to `PIL.Image.save <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save>`_.

    Return
    ------
    Image
        Return a new image pointed to the new URI.

    Example
    -------

    >>> spark.createDataFrame(..).registerTempTable("df")
    >>>
    >>> spark.sql(\"\"\"SELECT numpy_to_image(
    ...        resize(grayscale(image)),
    ...        lit('s3://asset')
    ...    ) AS new_image FROM df\"\"\")

    See Also
    --------
    :py:meth:`ligavision.dsl.vision.Image.from_array`
    """  # noqa: E501
    return Image.from_array(array, uri, format=format, **kwargs)


@udf(returnType=ArrayType(ImageType(), True))
def crop(img: Image, box: Union[Box2d, List[Box2d]]):
    """Crop image specified by the bounding boxes, and returns the cropped
    images.

    Parameters
    ----------
    img : Image
        An image object to be cropped.
    box : Box2d or List of Box2d
        One bound-2d box or a list of such boxes.

    Returns
    -------
    [Image]
        Return a list of cropped images.

    Examples
    --------

    >>> spark.sql("SELECT crop(img, boxes) as patches FROM detections")

    """
    return img.crop(box)
