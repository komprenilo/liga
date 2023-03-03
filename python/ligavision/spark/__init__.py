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

import os
from typing import Optional

from liga.logging import logger
from liga.spark import get_liga_assembly_jar
from liga.spark import init_session as liga_init_session

from ligavision.__version__ import version
from ligavision.spark.functions import init_udf


def get_liga_vision_jar(vision_type: str, jar_type: str, scala_version: str) -> str:
    name = f"liga-{vision_type}-assembly_{scala_version}"
    url = "https://github.com/liga-ai/ligavision/releases/download"
    github_jar = f"{url}/ligavision_{version}/{name}-{version}.jar"
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
            local_jar_path = f"{project_path}/out/{vision_type}/{scala_version}/assembly.dest/out.jar"
            if os.path.exists(local_jar_path):
                return local_jar_path
            else:
                raise ValueError("Please run `./mill 'image[2.12].assembly'` first")
        else:
            logger.warning(
                "Jar type `local` is for developing purpose, fallback to Jar"
                " type `github` because no project root is specified"
            )
            return github_jar
    else:
        raise ValueError(f"Invalid jar_type ({jar_type})!")


def init_session(
    app_name="Liga Vision App",
    conf: Optional[dict] = None,
    jar_type="github",
    scala_version: str = "2.12",
    with_udf=True, 
):
    if conf and "spark.jars" in conf.keys():
        pass
    else:
        liga_image_uri = get_liga_vision_jar("image", jar_type, scala_version)
        if not conf:
            conf = {}
        conf["spark.jars"] = ",".join([liga_image_uri])
        conf["spark.sql.extensions"] = ",".join([
            "net.xmacs.liga.spark.RikaiSparkSessionExtensions",
            "org.apache.spark.sql.rikai.LigaImageExtensions"
        ])
    spark = liga_init_session(app_name=app_name, conf=conf)
    if with_udf:
        init_udf(spark)
    return spark
    