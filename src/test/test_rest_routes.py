from unittest.mock import patch

from fastapi.testclient import TestClient
from fastapi import status

from src.rest import routes
from src.rest.server import app

client = TestClient(app=app)


@patch.object(routes, "valueset_mapper")
def test_fetch_valueset_by_accession_id(valueset_mapper):
    valueset_mapper.return_value = response1()
    response = client.get("/api/valuesets/accession_id/mane.select")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response1()
    valueset_mapper.assert_called_once()


def test_fetch_valueset_by_accession_id_not_found():
    response = client.get("/api/valuesets/accession_id/mane.selet")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Valueset doesn't exists for accession id : mane.selet"}


@patch.object(routes, "valueset_result_mapper")
def test_fetch_valuesets_by_value(valueset_result_mapper):
    valueset_result_mapper.return_value = response2()
    response = client.get("/api/valuesets/value/amino_acid_alphabet", params={"is_current": "true"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response2()
    valueset_result_mapper.assert_called_once()


def test_fetch_valuesets_by_value_not_found():
    response = client.get("/api/valuesets/value/amino_acid_alp", params={"is_current": "true"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Valueset doesn't exists for value : amino_acid_alp and is_current : True"
    }


@patch.object(routes, "valueset_result_mapper")
def test_fetch_all_valuesets(valueset_result_mapper):
    valueset_result_mapper.return_value = response2()
    response = client.get("/api/valuesets", params={"is_current": "true"})
    assert response.status_code == status.HTTP_200_OK
    assert any(obj == response2()[0] for obj in response.json())
    valueset_result_mapper.assert_called_once()


def response1():
    return {
        "accession_id": "mane.select",
        "label": "MANE Select",
        "value": "select",
        "is_current": True,
        "definition": "The Matched Annotation from NCBI and EMBL-EBI is a collaboration between Ensembl/GENCODE and RefSeq. The MANE Select is a default transcript per human gene that is representative of biology, well-supported, expressed and highly-conserved. This transcript set matches GRCh38 and is 100% identical between RefSeq and Ensembl/GENCODE for 5' UTR, CDS, splicing and 3'UTR.",
        "description": "",
    }


def response2():
    return [
        {
            "accession_id": "alphabet.amino_acid",
            "label": "Amino acid notation",
            "value": "amino_acid_alphabet",
            "is_current": True,
            "definition": "IUPAC notation for amino acids",
            "description": "One letter representation of amino acids inline with the IUPAC specification.",
        }
    ]
