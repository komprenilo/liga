#  Copyright (c) 2021 Rikai Authors
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

"""Custom Mlflow model logger to make sure models have the right logging for
Rikai SQL ML
"""

import tempfile
import warnings
from typing import Any, Optional

from liga.mlflow import *


class MlflowLogger:
    """
    An alternative model logger for use during training instead of the vanilla
    mlflow logger.

    """

    _CURRENT_MODEL_SPEC_VERSION = "1.0"

    def __init__(self, flavor: str):
        """
        Parameters
        ----------
        flavor: str
            The model flavor
        """
        self.spec_version = MlflowLogger._CURRENT_MODEL_SPEC_VERSION
        self.flavor = flavor

    def log_model(
        self,
        model: Any,
        artifact_path: str,
        schema: Optional[str] = None,
        registered_model_name: Optional[str] = None,
        liga_plugin_name: Optional[str] = None,
        model_type: Optional[str] = None,
        labels: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        """Convenience function to log the model with tags needed by rikai.
        This should be called during training when the model is produced.

        Parameters
        ----------
        model: Any
            The model artifact object
        artifact_path: str
            The relative (to the run) artifact path
        schema: str
            Output schema (pyspark DataType)
        registered_model_name: str, default None
            Model name in the mlflow model registry
        model_type : str
            Model type
        kwargs: dict
            Passed to `mlflow.<flavor>.log_model`


        Examples
        --------

        .. code-block:: python

            import rikai.mlflow

            # Log PyTorch model
            with mlflow.start_run() as run:

                # Training loop
                # ...

                # Assume `model` is the trained model from the training loop
                rikai.mlflow.pytorch.log_model(model, "model",
                        model_type="ssd",
                        registered_model_name="MyPytorchModel")


        For more details see `mlflow docs <https://www.mlflow.org/docs/latest/python_api/mlflow.pytorch.html#mlflow.pytorch.log_model>`_.
        """  # noqa E501

        try:
            import mlflow
            from mlflow.tracking import MlflowClient
        except ImportError as e:
            raise ImportError(
                "Couldn't import mlflow. Please make sure to "
                "`pip install mlflow` explicitly or install "
                "the correct extras like `pip install rikai[mlflow]`"
            ) from e

        # no need to set the tracking uri here since this is intended to be
        # called inside the training loop within mlflow.start_run
        getattr(mlflow, self.flavor).log_model(
            model,
            artifact_path,
            registered_model_name=registered_model_name,
            **kwargs,
        )

        tags = {
            CONF_MLFLOW_SPEC_VERSION: MlflowLogger._CURRENT_MODEL_SPEC_VERSION,
            CONF_MLFLOW_MODEL_PLUGIN: liga_plugin_name
            if liga_plugin_name
            else self.flavor,
            CONF_MLFLOW_MODEL_TYPE: model_type,
            CONF_MLFLOW_OUTPUT_SCHEMA: schema,
            CONF_MLFLOW_ARTIFACT_PATH: artifact_path,
        }
        if labels:
            if labels.get("uri"):
                tags[CONF_MLFLOW_LABEL_URI] = labels.get("uri")
            elif labels.get("func"):
                tags[CONF_MLFLOW_LABEL_FUNC] = labels.get("func")

        for k in (
            CONF_MLFLOW_MODEL_TYPE,
            CONF_MLFLOW_OUTPUT_SCHEMA,
        ):
            if not tags[k]:
                del tags[k]
                warnings.warn(
                    f"value of {k} is None or empty and "
                    "will not be populated to MLflow"
                )
        mlflow.set_tags(tags)
        if registered_model_name is not None:
            # if we're creating a model registry entry,
            # we also want to set the tags on the model version
            # and model to enable search
            c = MlflowClient()
            # mlflow log_model does not return the version (wtf)
            all_versions = c.get_latest_versions(
                registered_model_name, stages=["production", "staging", "None"]
            )
            current_version = None
            run_id = mlflow.active_run().info.run_id
            for v in all_versions:
                if v.run_id == run_id:
                    current_version = v
                    break
            if current_version is None:
                raise ValueError(
                    "No model version found matching runid: {}".format(run_id)
                )
            for key, value in tags.items():
                c.set_registered_model_tag(registered_model_name, key, value)
                c.set_model_version_tag(
                    registered_model_name, current_version.version, key, value
                )


KNOWN_FLAVORS = ["pytorch", "sklearn"]
for flavor in KNOWN_FLAVORS:
    globals()[flavor] = MlflowLogger(flavor)
