from src.common.config import default_conf
from src.common.valuesets_data import ValueSetData


value_sets_data = ValueSetData(default_conf, autoload=True)


async def get_value_sets_data():
    return value_sets_data
