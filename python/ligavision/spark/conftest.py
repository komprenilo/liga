import pytest
from pathlib import Path

from pyspark.sql import SparkSession

from ligavision.spark.types import Image
from ligavision.spark import init_session


@pytest.fixture(scope="session")
def two_flickr_images() -> list:
    return [
        Image.read(uri)
        for uri in [
            "http://farm2.staticflickr.com/1129/4726871278_4dd241a03a_z.jpg",
            "http://farm4.staticflickr.com/3726/9457732891_87c6512b62_z.jpg",
        ]
    ]

@pytest.fixture(scope="module")
def spark(tmp_path_factory) -> SparkSession:
    warehouse_path = tmp_path_factory.mktemp("warehouse")
    return init_session(jar_type="local")

@pytest.fixture
def asset_path() -> Path:
    import os
    project_path = os.environ.get("ROOTDIR")
    return Path(project_path) / "video" / "test" / "resources"
