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

import re
import os
from importlib.metadata import version as find_version
from typing import Optional

from pyspark.sql import SparkSession

from liga.__version__ import version
from liga.logging import logger


def get_default_jar_version(use_snapshot: bool = True) -> str:
    """
    Make it easier to reference the jar version in notebooks and conftest.

    Parameters
    ----------
    use_snapshot: bool, default True
        If True then map `*dev0` versions to `-SNAPSHOT`
    """
    pattern = re.compile(r"([\d]+.[\d]+.[\d]+)")
    match = re.search(pattern, version)
    if not match:
        raise ValueError(f"Ill-formed version string {version}")
    match_str = match.group(1)
    if use_snapshot and (len(match_str) < len(version)):
        return match_str + "-SNAPSHOT"
    return match_str


def get_liga_assembly_jar(jar_type: str, scala_version: str) -> str:
    spark_version = find_version("pyspark").replace(".", "")
    name = f"liga-spark{spark_version}-assembly_{scala_version}"
    url = "https://github.com/liga-ai/liga/releases/download"
    github_jar = f"{url}/v{version}/{name}-{version}.jar"
    if jar_type == "github":
        if "dev" in version:
            logger.warning(
                "Jar type `github` is for stable release, "
                "it may fail when version contains dev"
            )
        return github_jar
    elif jar_type == "local":
        project_path = os.environ.get("ROOTDIR")
        if project_path:
            local_jar_path = f"{project_path}/target/scala-{scala_version}"
            snapshot = (
                f"{local_jar_path}/{name}-{get_default_jar_version()}.jar"
            )
            dev = f"{local_jar_path}/{name}-{version}.jar"
            if os.path.exists(snapshot):
                return snapshot
            elif os.path.exists(dev):
                return dev
            else:
                raise ValueError("Please run `sbt clean assembly` first")
        else:
            logger.warning(
                "Jar type `local` is for developing purpose, fallback to Jar"
                " type `github` because no project root is specified"
            )
            return github_jar
    else:
        raise ValueError(f"Invalid jar_type ({jar_type})!")


def init_session(
    conf: Optional[dict] = None,
    app_name: str = "Liga",
    num_cores: int = 2,
    jar_type: str = "github",
    scala_version: str = "2.12",
) -> SparkSession:
    import sys

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    default_conf = {
        "spark.sql.extensions": "net.xmacs.liga.spark.RikaiSparkSessionExtensions",
        "spark.driver.extraJavaOptions": "-Dio.netty.tryReflectionSetAccessible=true",
        "spark.executor.extraJavaOptions": "-Dio.netty.tryReflectionSetAccessible=true",
    }

    if conf and "spark.jars" in conf.keys():
        pass
    else:
        default_conf["spark.jars"] = get_liga_assembly_jar(
            jar_type, scala_version
        )

    if conf:
        for k, v in conf.items():
            default_conf[k] = v

    # Avoid reused session polluting configs
    active_session = SparkSession.getActiveSession()
    if active_session:
        for k, v in default_conf.items():
            if v is not None and str(active_session.conf.get(k)) != str(v):
                print(
                    f"active session: want {v} for {k}"
                    f" but got {active_session.conf.get(k)},"
                    f" will restart session"
                )
                active_session.stop()
                break

    builder = SparkSession.builder.appName(app_name)
    for k, v in default_conf.items():
        if v is not None:
            builder = builder.config(k, v)
            logger.info(f"setting {k} to {v}")
    session = builder.master(f"local[{num_cores}]").getOrCreate()
    return session


def init_dbr_session(app_name="Liga on Databricks"):
    return init_session(conf={"spark.jars": None}, app_name=app_name)
