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

from ensembl.valuesets.valuesets_data import ValueSetData
from ensembl.valuesets.config import Config
from ensembl.valuesets.valuesets_rpc_server import ValueSetGetterServicer
from ensembl.valuesets.valuesets_pb2 import ValueSetRequest

from urllib.parse import urlparse

@pytest.fixture(scope='module')
def valueset_data():
    conf = Config(
        debug=False,
        server_port=50051,
        vset_source=urlparse('file:./src/python/tests/data/valuesets.json'),
        max_workers=10,
        stop_timeout=30,
        request_timeout=10
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
    return ValueSetRequest(
                accession_id = 'mane.plus_clinical',
                value = 'plus_clinical',
                is_current = True
    )

@pytest.fixture
def vs_request_domain_current_ok():
    return ValueSetRequest(
                accession_id = 'mane',
                is_current = True,
    )

@pytest.fixture
def vs_request_noncurr_ok():
    return ValueSetRequest(
                accession_id = 'mane.plus_clinical2',
                value = 'plus_clinical'
    )

@pytest.fixture
def vs_request_domain_noncurr_ok():
    return ValueSetRequest(
                accession_id = 'mane',
    )

@pytest.fixture
def vs_request_missing():
    return ValueSetRequest(
                accession_id = 'mane.minus_clinical',
                value = 'minus_clinical'
    )


def test_get_vs_by_accession_success(vs_servicer, vs_request_current_ok, context):
    response = vs_servicer.GetValueSetByAccessionId(request=vs_request_current_ok, context=context)
    vset = response.valuesets[0]
    assert len(response.valuesets) == 1
    assert vset.accession_id == vs_request_current_ok.accession_id
    assert vset.value == vs_request_current_ok.value
    assert vset.is_current

def test_get_vs_by_accession_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetByAccessionId(request=vs_request_missing, context=context)
    assert len(response.valuesets) == 0

def test_get_vs_by_value_current_success(vs_servicer, vs_request_current_ok, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_current_ok, context=context)
    vsets = response.valuesets
    assert len(vsets) == 1
    assert vsets[0].accession_id == vs_request_current_ok.accession_id
    assert vsets[0].value == vs_request_current_ok.value
    assert vsets[0].is_current

def test_get_vs_by_value_success(vs_servicer, vs_request_noncurr_ok, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_noncurr_ok, context=context)
    assert len(response.valuesets) == 2
    check = 0
    for v in response.valuesets:
        assert v.value == vs_request_noncurr_ok.value
        check += 1 if v.is_current else -1
    assert check == 0

def test_get_vs_by_value_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetsByValue(request=vs_request_missing, context=context)
    assert len(response.valuesets) == 0

def test_get_vs_by_domain_current_success(vs_servicer, vs_request_domain_current_ok, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_domain_current_ok, context=context)
    assert len(response.valuesets) == 2
    for v in response.valuesets:
        assert vs_request_domain_current_ok.accession_id in v.accession_id
        assert v.is_current

def test_get_vs_by_domain_success(vs_servicer, vs_request_domain_noncurr_ok, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_domain_noncurr_ok, context=context)
    assert len(response.valuesets) == 4
    check = 0
    for v in response.valuesets:
        assert vs_request_domain_noncurr_ok.accession_id in v.accession_id
        check += 1 if v.is_current else -1
    assert check == 0

def test_get_vs_by_domain_missing(vs_servicer, vs_request_missing, context):
    response = vs_servicer.GetValueSetsByDomain(request=vs_request_missing, context=context)
    assert len(response.valuesets) == 0


def test_get_all_current(vs_servicer, vs_request_domain_current_ok, context):
    response = vs_servicer.GetAllValueSets(request=vs_request_domain_current_ok, context=context)
    for cnt,vset in enumerate(response, start=1):
        assert vset.is_current
    assert cnt == 29

def test_get_all(vs_servicer, vs_request_domain_noncurr_ok, context):
    response = vs_servicer.GetAllValueSets(request=vs_request_domain_noncurr_ok, context=context)
    cnt_noncurr = 0
    for cnt,vset in enumerate(response, start=1):
        cnt_noncurr += 0 if vset.is_current else 1
    assert cnt == 31
    assert cnt_noncurr == 2