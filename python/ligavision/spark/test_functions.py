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

"""Unit tests for Rikai provided spark UDFs."""

from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pandas.testing as pdt
from PIL import Image as PILImage
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col, concat, lit
from pyspark.sql.types import ArrayType, StructField, StructType

# Rikai
from liga.numpy import view
from ligavision.spark.functions import (
    area,
    box2d,
    box2d_from_center,
    crop,
    numpy_to_image,
    to_image,
)
from ligavision.spark.types.geometry import Box2dType
from ligavision.spark.types import ImageType, Image, Box2d


def test_init(spark):
    rikai_udf_names = [
        x.name
        for x in spark.catalog.listFunctions()
        if x.className.startswith("org.apache.spark.sql.UDFRegistration")
    ]
    assert "area" in rikai_udf_names
    assert "copy" in rikai_udf_names
    assert "to_image" in rikai_udf_names
    assert len(rikai_udf_names) > 6


def assert_area_equals(array, df):
    pdt.assert_frame_equal(
        pd.DataFrame({"area": array}),
        df.select("area").toPandas(),
        check_dtype=False,
    )


def test_areas(spark: SparkSession):
    """Test calculating bounding box's area."""
    df = spark.createDataFrame(
        [
            (Box2d(1, 2, 2.0, 3.0),),
            (Box2d(10, 12, 11.0, 17.0),),
        ],
        ["bbox"],
    )
    df = df.withColumn("area", area(col("bbox")))
    assert_area_equals([1.0, 5.0], df)


def test_box2d_udfs(spark):
    df = spark.createDataFrame(
        [
            Row(values=[1.0, 2.0, 2.0, 3.0]),
            Row(values=[10.0, 12.0, 11.0, 17.0]),
        ],
        ["values"],
    ).withColumn("bbox", box2d("values"))
    df = df.withColumn("area", area(col("bbox")))
    assert_area_equals([1.0, 5.0], df)


def test_box2d_center(spark):
    df = spark.createDataFrame(
        [
            Row(values=[1.5, 2.5, 1.0, 1.0]),
            Row(values=[10.5, 14.5, 1.0, 5.0]),
        ],
        ["values"],
    ).withColumn("bbox", box2d_from_center("values"))
    df = df.withColumn("area", area(col("bbox")))
    assert_area_equals([1.0, 5.0], df)


def test_box2d_top_left(spark: SparkSession):
    df = spark.createDataFrame(
        [
            Row(values=[1.0, 2.0, 1.0, 1.0]),
            Row(values=[10.0, 12.0, 1.0, 5.0]),
        ],
        ["values"],
    ).withColumn("bbox", box2d_from_center("values"))
    df = df.withColumn("area", area(col("bbox")))
    assert_area_equals([1.0, 5.0], df)


def test_to_image(spark: SparkSession, asset_path: Path):
    """Test casting from data into Image asset."""
    image_uri = str(asset_path / "test_image.jpg")
    image = PILImage.open(image_uri)

    image_bytes = BytesIO()
    image.save(image_bytes, format="png")
    image_bytes = image_bytes.getvalue()
    image_byte_array = bytearray(image_bytes)

    df1 = spark.createDataFrame([Row(values=image_uri)], ["image_uri"])
    df2 = spark.createDataFrame([Row(values=image_bytes)], ["image_bytes"])
    df3 = spark.createDataFrame(
        [Row(values=image_byte_array)], ["image_byte_array"]
    )

    df1 = df1.withColumn("image", to_image(col("image_uri")))
    df2 = df2.withColumn("image", to_image(col("image_bytes")))
    df3 = df3.withColumn("image", to_image(col("image_byte_array")))

    uri_sample = df1.first()["image"]
    bytes_sample = df2.first()["image"]
    byte_array_sample = df3.first()["image"]

    assert type(uri_sample) == Image
    assert type(bytes_sample) == Image
    assert type(byte_array_sample) == Image


def test_numpy_to_image(spark: SparkSession, tmp_path: Path):
    """Test upload a numpy image to the external storage,
    and convert the data into Image asset.

    """
    df = spark.createDataFrame(
        [Row(id=1, data=view(np.ones((32, 32), dtype=np.uint8)))]
    )
    df = df.withColumn(
        "image",
        numpy_to_image(
            df.data, concat(lit(str(tmp_path)), lit("/"), df.id, lit(".png"))
        ),
    )
    df.count()
    # print(df.first().image)
    assert Path(df.first().image.uri) == tmp_path / "1.png"
    assert (tmp_path / "1.png").exists()


def test_crops(spark: SparkSession, tmp_path: Path, two_flickr_images: list):
    img = two_flickr_images[0]
    data = img.to_numpy()
    df = spark.createDataFrame(
        [
            {
                "img": img,
                "boxes": [
                    Box2d(10, 10, 30, 30),
                    Box2d(15, 15, 35, 35),
                    Box2d(20, 20, 40, 40),
                ],
            }
        ],
        schema=StructType(
            [
                StructField("img", ImageType()),
                StructField("boxes", ArrayType(Box2dType())),
            ]
        ),
    ).withColumn("patches", crop("img", "boxes"))
    patches = df.first().patches
    assert len(patches) == 3
    assert np.array_equal(patches[0].to_numpy(), data[10:30, 10:30, :])
    assert np.array_equal(patches[1].to_numpy(), data[15:35, 15:35, :])
    assert np.array_equal(patches[2].to_numpy(), data[20:40, 20:40, :])
