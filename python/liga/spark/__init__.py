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
from importlib.metadata import version as find_version

from liga.__version__ import version
from liga.logging import logger


def get_default_jar_version(use_snapshot=True):
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
        raise ValueError("Ill-formed version string {}".format(version))
    match_str = match.group(1)
    if use_snapshot and (len(match_str) < len(version)):
        return match_str + "-SNAPSHOT"
    return match_str


def _liga_assembly_jar(jar_type: str, scala_version: str):
    spark_version = find_version("pyspark").replace(".", "")
    name = f"liga-spark{spark_version}-assembly_{scala_version}"
    url = "https://github.com/liga-ai/liga/releases/download"
    github_jar = f"{url}/v{version}/{name}-{version}.jar"
    if jar_type == "github":
        return github_jar
    elif jar_type == "local":
        if "dev" not in version:
            logger.info("Jar type `local` is for developing purpose, use Jar on Github instead")
            return github_jar
        else:
            import os

            project_path = os.environ["ROOTDIR"]
            return f"{project_path}/target/scala-{scala_version}/{name}-{get_default_jar_version()}.jar"
    else:
        raise ValueError(f"Invalid jar_type ({jar_type})!")


def init(
    conf: dict = None,
    app_name="Liga",
    scala_version="2.12",
    num_cores=2,
    jar_type="github",
):
    from pyspark.sql import SparkSession
    import os
    import sys

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    # Avoid reused session polluting configs
    active_session = SparkSession.getActiveSession()
    if active_session and conf:
        for k, v in conf.items():
            if str(active_session.conf.get(k)) != str(v):
                print(
                    f"active session: want {v} for {k}"
                    f" but got {active_session.conf.get(k)},"
                    f" will restart session"
                )
                active_session.stop()
                break

    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.jars", _liga_assembly_jar(jar_type, scala_version))
        .config(
            "spark.sql.extensions",
            "ai.eto.rikai.sql.spark.RikaiSparkSessionExtensions",
        )
        .config(
            "spark.driver.extraJavaOptions",
            "-Dio.netty.tryReflectionSetAccessible=true",
        )
        .config(
            "spark.executor.extraJavaOptions",
            "-Dio.netty.tryReflectionSetAccessible=true",
        )
    )
    conf = conf or {}
    for k, v in conf.items():
        builder = builder.config(k, v)
    session = builder.master(f"local[{num_cores}]").getOrCreate()
    return session
