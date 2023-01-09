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

import logging

_LOG_FORMAT = (
    "%(asctime)s %(levelname)s %(name)s (%(filename)s:%(lineno)d): %(message)s"
)

__all__ = ["logger"]


def _set_logger(level: int = logging.INFO) -> logging.Logger:
    l = logging.getLogger("Rikai")
    l.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    l.handlers.clear()
    l.addHandler(handler)

    l.propagate = False
    return l


logger: logging.Logger = _set_logger()
