#  See the NOTICE file distributed with this work for additional information
#  regarding copyright ownership.
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
from common.valuesets_data import ValueSetData
from common.config import Config
from urllib.parse import urlparse


@pytest.fixture(scope="module")
def valueset_data():
    conf = Config(
        debug=False,
        server_port=50051,
        vset_source=urlparse("file:./src/test/data/valuesets.json"),
        max_workers=10,
        stop_timeout=30,
        request_timeout=10,
    )
    return ValueSetData(autoload=True, config=conf)


def test_fetch_data_from_json_url_https_ok(valueset_data):
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-valuesets/experimental/test-vsets/valuesets.json"
    vs_data = valueset_data.fetch_vs_data_from_json(urlparse(url))
    assert len(vs_data) > 0, "Got 0 valuesets"


def test_fetch_data_from_json_url_file_ok(valueset_data):
    url = "file:./src/test/data/valuesets.json"
    vs_data = valueset_data.fetch_vs_data_from_json(urlparse(url))
    assert len(vs_data) > 0, "Got 0 valuesets"


def test_fetch_data_from_json_url_ko_str(valueset_data):
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-valuesets/experimental/test-vsets/valuesets.json"
    with pytest.raises(ValueError) as e_info:
        _ = valueset_data.fetch_vs_data_from_json(url)


def test_fetch_data_from_json_url_ko_scheme(valueset_data):
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-valuesets/experimental/test-vsets/valuesets.json"
    with pytest.raises(ValueError) as e_info:
        _ = valueset_data.fetch_vs_data_from_json(url)


def test_fetch_data_from_json_url_file_ko(valueset_data):
    url = "file:./src/test/data/valueset.json"
    with pytest.raises(ValueError) as e_info:
        _ = valueset_data.fetch_vs_data_from_json(urlparse(url))


def test_fetch_data_from_json_url_https_ko(valueset_data):
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-valuesets/main/notsuchafile.json"
    with pytest.raises(Exception) as e_info:
        _ = valueset_data.fetch_vs_data_from_json(urlparse(url))


def test_get_vsdata_by_accession_id_ok(valueset_data):
    vs = valueset_data.get_vsdata_by_accession_id("mane.select.1")
    assert (
        vs.accession_id == "mane.select.1"
    ), f"Response accession_id: {vs.accession_id} not the expected one: mane.select.1"
    assert vs.label == "MANE Select", f"Response label: {vs.label} not the expected one: MANE.Select"
    assert vs.is_current == True, "Valueset returned is not current"


def test_get_vsdata_by_accession_id_none(valueset_data):
    vs = valueset_data.get_vsdata_by_accession_id("unknown.accession_id")
    assert isinstance(vs, tuple), "Valusets data returned is not of type 'tuple'"
    assert not vs, "Returned data while none is expected"


def test_get_vsdata_by_accession_id_empty(valueset_data):
    with pytest.raises(TypeError) as e_info:
        _ = valueset_data.get_vsdata_by_accession_id()


def test_get_vsdata_by_topic_current_ok(valueset_data):
    vs = valueset_data.get_vsdata_by_topic(topic="mane", is_current=True)
    vs_test = [v.accession_id for v in vs if v.accession_id in ("mane.select.1", "mane.plus_clinical.1")]
    assert len(vs) == 2 and len(vs_test) == 2, f"Got {len(vs)} valusets while expecting 2"


def test_get_vsdata_by_topic_ok(valueset_data):
    vs = valueset_data.get_vsdata_by_topic(topic="mane")
    vs_test = [
        v.accession_id
        for v in vs
        if v.accession_id in ("mane.select.1", "mane.plus_clinical.1") and v.is_current
    ]
    assert len(vs) == 3 and len(vs_test) == 2, f"Got {len(vs)} valusets while expecting 3"


def test_get_vsdata_by_topic_none(valueset_data):
    vs = valueset_data.get_vsdata_by_topic(topic="mone")
    assert isinstance(vs, tuple) and not vs, "Returned data while none is expected"


def test_get_vsdata_by_topic_empty(valueset_data):
    with pytest.raises(TypeError) as e_info:
        _ = valueset_data.get_vsdata_by_topic()


def test_get_all_current(valueset_data):
    vs = valueset_data.get_all(1)
    assert len(vs) == 16, f"Got {len(vs)} current valuesets while expecting 16"


def test_get_all(valueset_data):
    vs = valueset_data.get_all()
    vs_test = [v.accession_id for v in vs if v.is_current]
    assert len(vs) == 17 and len(vs_test) == 16, f"Got {len(vs)} current valuesets while expecting 17"
