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
"""
ValuSets ValueSetsGetter tests
"""

import pytest
import grpc

from src.common.valuesets_data import ValueSetData
from src.common.config import Config
from src.grpcapi.ensembl.server import ValueSetGetterServicer
from src.grpcapi.ensembl.valuesets.valuesets_pb2 import ValueSetRequest

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


class MockContext:
    def abort(self, status, msg):
        error = grpc.RpcError()
        error.code = lambda: status
        error.details = lambda: msg
        raise error


@pytest.fixture
def context():
    return MockContext()


@pytest.fixture
def vs_servicer(valueset_data):
    return ValueSetGetterServicer(valueset_data)


@pytest.fixture
def vs_request_current_ok():
    return ValueSetRequest(accession_id="mane.plus_clinical", value="plus_clinical", is_current=True)


@pytest.fixture
def vs_request_domain_current_ok():
    return ValueSetRequest(
        accession_id="mane",
        is_current=True,
    )


@pytest.fixture
def vs_request_noncurr_ok():
    return ValueSetRequest(accession_id="mane.plus_clinical2", value="plus_clinical")


@pytest.fixture
def vs_request_domain_noncurr_ok():
    return ValueSetRequest(
        accession_id="mane",
    )


@pytest.fixture
def vs_request_missing():
    return ValueSetRequest(accession_id="mane.minus_clinical", value="minus_clinical")


@pytest.fixture
def vs_request_empty():
    return ValueSetRequest()


def test_get_vs_by_accession_success(vs_servicer, vs_request_current_ok, context):
    response = vs_servicer.GetValueSetByAccessionId(request=vs_request_current_ok, context=context)
    vset = response.valuesets[0]
    assert len(response.valuesets) == 1, f"Got {len(response.valuesets)} valusets while expecting 1"
    assert (
        vset.accession_id == vs_request_current_ok.accession_id
    ), f"Response accession_id: {vset.accession_id} not the expected one: {vs_request_current_ok.accession_id}"
    assert (
        vset.value == vs_request_current_ok.value
    ), f"Response value: {vset.value} not the expected one: {vs_request_current_ok.value}"
    assert vset.is_current, "Valueset returned is not current"


def test_get_vs_by_accession_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetByAccessionId(request=vs_request_missing, context=context)
    assert (
        len(response.valuesets) == 0
    ), f"Got {len(response.valuesets)} valusets while expecting an empty response"


def test_get_vs_by_accession_error(vs_servicer, vs_request_empty, context):
    try:
        response = vs_servicer.GetValueSetByAccessionId(request=vs_request_empty, context=context)
    except grpc.RpcError as e:
        assert (
            e.code() == grpc.StatusCode.INVALID_ARGUMENT
        ), "Didn't raise the expected error INVALID_ARGUMENT"


def test_get_vs_by_value_current_success(vs_servicer, vs_request_current_ok, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_current_ok, context=context)
    vset = response.valuesets[0]
    assert len(response.valuesets) == 1, f"Got {len(response.valuesets)} valusets while expecting 1"
    assert (
        vset.accession_id == vs_request_current_ok.accession_id
    ), f"Response accession_id: {vset.accession_id} not the expected one: {vs_request_current_ok.accession_id}"
    assert (
        vset.value == vs_request_current_ok.value
    ), f"Response value: {vset.value} not the expected one: {vs_request_current_ok.value}"
    assert vset.is_current, "Valueset returned is not current"


def test_get_vs_by_value_success(vs_servicer, vs_request_noncurr_ok, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_noncurr_ok, context=context)
    assert len(response.valuesets) == 2, f"Got {len(response.valuesets)} valusets while expecting 2"
    check = 0
    for v in response.valuesets:
        assert (
            v.value == vs_request_noncurr_ok.value
        ), f"Value: {v.value} not the expected one: {vs_request_noncurr_ok.value}"
        check += 1 if v.is_current else -1
    assert check == 0


def test_get_vs_by_value_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_missing, context=context)
    assert (
        len(response.valuesets) == 0
    ), f"Got {len(response.valuesets)} valusets while expecting an empty response"


def test_get_vs_by_value_error(vs_servicer, vs_request_empty, context):
    try:
        response = vs_servicer.GetValueSetsByValue(request=vs_request_empty, context=context)
    except grpc.RpcError as e:
        assert (
            e.code() == grpc.StatusCode.INVALID_ARGUMENT
        ), "Didn't raise the expected error INVALID_ARGUMENT"


def test_get_vs_by_domain_current_success(vs_servicer, vs_request_domain_current_ok, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_domain_current_ok, context=context)
    assert len(response.valuesets) == 2, f"Got {len(response.valuesets)} valusets while expecting 2"
    for v in response.valuesets:
        assert (
            vs_request_domain_current_ok.accession_id in v.accession_id
        ), f"Response accession_id: {v.accession_id} does not include the domain: {vs_request_domain_current_ok.accession_id}"
        assert v.is_current, "Valueset returned is not current"


def test_get_vs_by_domain_success(vs_servicer, vs_request_domain_noncurr_ok, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_domain_noncurr_ok, context=context)
    assert len(response.valuesets) == 4, f"Got {len(response.valuesets)} valusets while expecting 4"
    check = 0
    for v in response.valuesets:
        assert (
            vs_request_domain_noncurr_ok.accession_id in v.accession_id
        ), f"Response accession_id: {v.accession_id} does not include the domain: {vs_request_domain_noncurr_ok.accession_id}"
        check += 1 if v.is_current else -1
    assert check == 0


def test_get_vs_by_domain_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_missing, context=context)
    assert (
        len(response.valuesets) == 0
    ), f"Got {len(response.valuesets)} valusets while expecting an empty response"


def test_get_vs_by_domain_error(vs_servicer, vs_request_empty, context):
    try:
        response = vs_servicer.GetValueSetsByDomain(request=vs_request_empty, context=context)
    except grpc.RpcError as e:
        assert (
            e.code() == grpc.StatusCode.INVALID_ARGUMENT
        ), "Didn't raise the expected error INVALID_ARGUMENT"


def test_get_vs_malformed_request(vs_servicer, context):
    try:
        request = ValueSetRequest(access_id="mane.plus_clinical")
    except ValueError:
        assert True, "Didn't raise the expected exception: ValueError"


def test_get_all_current(vs_servicer, vs_request_domain_current_ok, context):
    response = vs_servicer.GetAllValueSets(request=vs_request_domain_current_ok, context=context)
    for cnt, vset in enumerate(response, start=1):
        assert vset.is_current, "Valueset returned is not current"
    assert cnt == 29, f"Got {cnt} current valusets while expecting 29"


def test_get_all(vs_servicer, vs_request_domain_noncurr_ok, context):
    response = vs_servicer.GetAllValueSets(request=vs_request_domain_noncurr_ok, context=context)
    cnt_noncurr = 0
    for cnt, vset in enumerate(response, start=1):
        cnt_noncurr += 0 if vset.is_current else 1
    assert cnt == 31, f"Got {cnt} valusets while expecting 31"
    assert cnt_noncurr == 2, f"Got {cnt_noncurr} non current valusets while expecting 2"
