#  Copyright 2021 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import base64
from io import BytesIO
from pathlib import Path

import numpy as np
import requests
import requests_mock

from liga.io import exists


def test_simple_http_credentials():
    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", text="{}")
        requests.get("http://test.com", auth=("user", "def_not_pass"))
        req = mock.request_history[0]
        assert req.headers.get("Authorization") == "Basic {}".format(
            base64.b64encode(b"user:def_not_pass").decode("utf-8")
        )


def test_no_http_credentials():
    with requests_mock.Mocker() as mock:
        mock.get("http://test.com", text="{}")
        requests.get("http://test.com")
        req = mock.request_history[0]
        assert "Authorization" not in req.headers


def test_exists(tmp_path: Path):
    assert exists(str(tmp_path / "a.json")) is False
    with (tmp_path / "a.txt").open(mode="w") as fobj:
        fobj.write("blabla")
    assert exists(str(tmp_path / "a.txt"))
