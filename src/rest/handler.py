from typing import Any

from src.common.config import default_conf
from src.common.valuesets_data import ValueSetData
from src.rest.model import ValueSetItem


async def get_value_sets_data():
    return ValueSetData(default_conf, autoload=True)


def valueset_result_mapper(data: tuple[Any]) -> list[ValueSetItem]:
    result = []
    for item in data:
        vs_item = valueset_mapper(item)
        result.append(vs_item)
    return result


def valueset_mapper(value_set: Any) -> ValueSetItem:
    is_current = value_set.is_current if value_set.is_current != "" else False
    return ValueSetItem(
        accession_id=value_set.accession_id,
        label=value_set.label,
        value=value_set.value,
        is_current=is_current,
        definition=value_set.definition,
        description=value_set.description,
    )
