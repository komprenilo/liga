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

import warnings
from pathlib import Path
from urllib.parse import urlparse

warnings.filterwarnings("ignore", category=DeprecationWarning)  # noqa

# Third Party
import mlflow
import pytest
from mlflow.tracking import MlflowClient
from pyspark.sql import Row, SparkSession

from liga.spark import init_session
from liga.mlflow import CONF_MLFLOW_TRACKING_URI
from liga.__version__ import version


@pytest.fixture(scope="session")
def mlflow_client_with_tracking_uri(tmp_path_factory) -> (MlflowClient, str):
    tmp_path = tmp_path_factory.mktemp("mlflow")
    tmp_path.mkdir(parents=True, exist_ok=True)
    tracking_uri = "sqlite:///" + str(tmp_path / "tracking.db")
    mlflow.set_tracking_uri(tracking_uri)

    return mlflow.tracking.MlflowClient(tracking_uri), tracking_uri


@pytest.fixture(scope="session")
def mlflow_client(mlflow_client_with_tracking_uri):
    return mlflow_client_with_tracking_uri[0]


@pytest.fixture(scope="session")
def mlflow_tracking_uri(mlflow_client_with_tracking_uri):
    return mlflow_client_with_tracking_uri[1]


@pytest.fixture(scope="module")
def spark(mlflow_tracking_uri: str, tmp_path_factory) -> SparkSession:
    print(f"mlflow tracking uri for spark: ${mlflow_tracking_uri}")
    warehouse_path = tmp_path_factory.mktemp("warehouse")

    return init_session(
        dict(
            [
                ("spark.port.maxRetries", 128),
                ("spark.sql.warehouse.dir", str(warehouse_path)),
                (
                    "spark.rikai.sql.ml.registry.test.impl",
                    "net.xmacs.rikai.sql.model.testing.TestRegistry",
                ),
                (
                    CONF_MLFLOW_TRACKING_URI,
                    mlflow_tracking_uri,
                ),
                (
                    "spark.rikai.sql.ml.catalog.impl",
                    "net.xmacs.rikai.sql.model.SimpleCatalog",
                ),
            ]
        ),
        jar_type="local" if "dev" in version else "github",
    )


@pytest.fixture
def asset_path() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def sklearn_lr_uri(mlflow_tracking_uri, tmp_path_factory):
    from sklearn.datasets import load_diabetes
    from sklearn.linear_model import LinearRegression
    from liga.sklearn.mlflow import log_model

    X, y = load_diabetes(return_X_y=True)
    (X.shape, y.shape)

    mlflow.set_tracking_uri(mlflow_tracking_uri)

    # train a model
    model = LinearRegression()
    with mlflow.start_run() as run:
        model.fit(X, y)

        registered_model_name = f"sklearn_lr"
        log_model(model, registered_model_name)
        return f"mlflow:///{registered_model_name}"
