from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.rest.model import ValueSetItem
from src.common.valuesets_data import ValueSetData
from src.rest.handler import get_value_sets_data, valueset_mapper, valueset_result_mapper

router = APIRouter(prefix="/api")


@router.get("/valuesets/accession_id/{accession_id}", response_model=ValueSetItem)
async def fetch_valueset_by_accession_id(
    accession_id: str, vs_data: ValueSetData = Depends(get_value_sets_data)
) -> ValueSetItem:
    data = vs_data.get_vsdata_by_accession_id(accession_id)
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Valueset doesn't exists for accession id : {accession_id}"
        )
    return valueset_mapper(data)


@router.get("/valuesets/value/{value}", response_model=List[ValueSetItem])
async def fetch_valuesets_by_value(
    value: str, is_current: bool = False, vs_data: ValueSetData = Depends(get_value_sets_data)
) -> list[ValueSetItem]:
    data = vs_data.get_vsdata_by_value(value, is_current)
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Valueset doesn't exists for value : {value} and is_current : {is_current}",
        )
    return valueset_result_mapper(data)


@router.get("/valuesets", response_model=List[ValueSetItem])
async def fetch_all_valuesets(
    is_current: bool = False, vs_data: ValueSetData = Depends(get_value_sets_data)
) -> list[ValueSetItem]:
    data = vs_data.get_all(is_current)
    if not data:
        raise HTTPException(status_code=404, detail=f"Valuesets doesn't exists. is_current : {is_current}")
    return valueset_result_mapper(data)
