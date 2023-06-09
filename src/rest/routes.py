from typing import List

from fastapi import APIRouter, Depends, HTTPException

from rest.model import ValueSetItem
from common.valuesets_data import ValueSetData
from rest.handler import get_value_sets_data, valueset_mapper, valueset_result_mapper

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


@router.get("/valuesets/topic/{topic}", response_model=List[ValueSetItem])
async def fetch_valueset_by_topic(
    topic: str, vs_data: ValueSetData = Depends(get_value_sets_data)
) -> ValueSetItem:
    data = vs_data.get_vsdata_by_topic(topic, is_current=True)
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Valueset doesn't exists for topic : {topic}"
        )
    return valueset_mapper(data)


@router.get("/valuesets", response_model=List[ValueSetItem])
async def fetch_all_valuesets(
    is_current: bool = False, vs_data: ValueSetData = Depends(get_value_sets_data)
) -> list[ValueSetItem]:
    data = vs_data.get_all(is_current)
    if not data:
        raise HTTPException(status_code=404, detail=f"Valuesets doesn't exists. is_current : {is_current}")
    return valueset_result_mapper(data)
