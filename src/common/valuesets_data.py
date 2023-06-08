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


"""ValueSets Data.
Convenient class to load ValueSet data from remote JSON file
into a memory structure for the gRPC server
"""

import logging

from pathlib import Path
from urllib.parse import ParseResult
import json
import requests

import pandas as pd
from collections import namedtuple

from src.common.config import Config, default_conf

__all__ = ["ValueSetData"]

_logger = logging.getLogger(__name__)


class ValueSetData:
    """Provides methods that implement functionality of ValueSetData"""

    def __init__(self, config: Config = default_conf, autoload: bool = False) -> None:
        self._config = config
        self._data = None
        if autoload:
            self.load_data()

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    def load_data(self) -> None:
        data = self.fetch_vs_data_from_json(self._config.vset_source)
        self._load_data_into_cache(data)

    def _load_data_into_cache(self, vs_data_raw: dict) -> None:
        """Loads data fetched from JSON into memory Pandas DataFrame"""

        _logger.info("Loading in-memory cache")
        if not vs_data_raw:
            _logger.error("Something went wrong with loading the ValueSets")
            raise Exception("Something went wrong with loading the ValueSets")

        def make_row(key: str, vals: tuple[str]) -> tuple[str]:
            rr = [
                key,
            ]
            rr.extend(vals)
            return tuple(rr)

        values = [make_row(k, v) for k, v in vs_data_raw.items()]

        col_names = ["accession_id", "label", "value", "is_current", "definition", "description"]
        self._data = pd.DataFrame(values, index=vs_data_raw.keys(), columns=col_names)
        self._data["is_current"] = self._data["is_current"].replace([0, 1], [False, True])

    def fetch_vs_data_from_json(self, url: ParseResult = None) -> dict[str, tuple[str]]:
        """
        Fetches ValueSets from external JSON file.

        :param url: ParseResult object representing the URL of the json file
        :raise ValueError: if URL is not of type ParseResult
        :raise ValueError: if URL scheme is invalid (must be 'file', 'http', or 'https')
        :raise ValueError: if URL point to a file that does not exist
        :raise ValueError: if HTTP(s) URL GET fails
        :return: ValueSet data
        """

        if not url:
            url = self._config.vset_source
        if not isinstance(url, ParseResult):
            raise ValueError(f"Invalid input argument: {type(url)}")
        if url.scheme not in ("file", "http", "https"):
            _logger.error('Invalid scheme for valuesets URL; must be "file", "http", "https"')
            raise ValueError('Invalid scheme for valuesets URL; must be "file", "http", "https"')

        vs_data = {}
        if url.scheme == "file":
            _logger.debug("Loading JSON from file URL: %s", url.geturl())
            filename = Path(url.netloc) / Path(url.path)
            if not filename.exists() or not filename.is_file():
                _logger.error("Provided input filename %s does not exists or is not a file", url)
                raise ValueError(f"Provided input filename {url} does not exists or is not a file")
            with open(filename, "rt") as fh:
                vs_data = json.load(fh)
        else:
            _logger.debug("Loading JSON from http(s) URL: %s", url.geturl())
            r = requests.get(
                url.geturl(),
                headers={"Content-Type": "application/json"},
                timeout=self._config.request_timeout,
            )
            if not r.ok:
                _logger.error("Request failed with code %s", r.status_code)
                r.raise_for_status()
            print(r.content)
            vs_data = r.json()

        return vs_data

    def get_vsdata_by_accession_id(self, accession_id: str) -> namedtuple:
        """
        Retrieves ValueSet data from cache by accession.

        :param accession_id: The accession of the data to retrieve
        :return: ValueSet data
        """
        accession_id.lower()
        _logger.debug("Getting ValueSet data by accession %s", accession_id)
        vs = self._data.loc[self._data["accession_id"] == accession_id]
        res = tuple(vs.itertuples(name="ValueSet", index=False))
        return res[0] if res else tuple()

    def get_vsdata_by_value(self, value: str, is_current: bool = False) -> tuple[namedtuple]:
        """
        Retrieves ValueSet data from cache by value.

        :param value: The value of the data to retrieve
        :param is_current: The is_current flag of the data (default False)
        :return: ValueSet data
        """
        value.lower()
        curr_s = "current" if is_current else ""
        _logger.debug("Getting %s ValueSet data by value %s", curr_s, value)
        if is_current:
            vs = self._data.loc[(self._data["value"] == value) & (self._data["is_current"] == is_current)]
        else:
            vs = self._data.loc[self._data["value"] == value]
        res = tuple(vs.itertuples(name="ValueSet", index=False))
        return res if res else tuple()

    def get_vsdata_by_domain(self, domain: str, is_current: bool = False) -> tuple[namedtuple]:
        """
        Retrieves ValueSet data from cache by domain.

        :param domain: The domain of the data to retrieve
        :param is_current: The is_current flag of the data (default False)
        :return: ValueSet data
        """
        domain.lower()
        curr_s = "current" if is_current else ""
        _logger.debug("Getting %s ValueSet data by domain %s", curr_s, domain)
        if is_current:
            vs = self._data.loc[
                (self._data["accession_id"].str.startswith(domain)) & (self._data["is_current"] == is_current)
            ]
        else:
            vs = self._data.loc[self._data["accession_id"].str.contains(domain)]
        res = tuple(vs.itertuples(name="ValueSet", index=False))
        return res if res else tuple()

    def get_all(self, is_current: bool = False) -> tuple[namedtuple]:
        """
        Retrieves the whole ValueSet data from cache.

        :param is_current: The is_current flag of the data (default False)
        :return: ValueSet data
        """
        curr_s = "current" if is_current else ""
        _logger.debug("Getting all %s ValueSet data", curr_s)
        if is_current:
            vs = self._data.loc[self._data["is_current"] == is_current]
        else:
            vs = self._data
        res = tuple(vs.itertuples(name="ValueSet", index=False))
        return res if res else tuple()


if __name__ == "__main__":
    from urllib.parse import urlparse

    conf = Config(
        debug=False,
        server_port=50051,
        vset_source=urlparse("file:./src/python/tests/data/valuesets.json"),
        max_workers=10,
        stop_timeout=30,
        request_timeout=10,
    )
    vd = ValueSetData(config=conf, autoload=True)
    vs = vd.get_vsdata_by_domain(domain="mane", is_current=True)
    vs_test = [v.accession_id for v in vs if v.accession_id not in ("mane.select", "mane.plus_clinical")]
    for i in vs_test:
        print(i)
