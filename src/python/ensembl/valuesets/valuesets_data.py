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

import sys
from typing import Generator
from logging import Logger

from pathlib import Path
from urllib.parse import ParseResult
import json
import requests

import pandas as pd
from collections import namedtuple

from ensembl.valuesets.config import Config, default_conf


__all__ = [ 'ValueSetData' ]


class ValueSetData():

    def __init__(self, config: Config = default_conf, logger: Logger = None, autoload: bool = False) -> None:
        self._config = config
        self._logger = self.init_logger(logger=logger)
        self._data = None
        if autoload:
            self.load_data()


    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    
    def init_logger(self, logger: Logger = None) -> Logger:
        if logger is not None:
            return logger
        
        import logging
        logging.basicConfig(
            stream=sys.stdout,
            format="%(asctime)s %(levelname)-8s %(name)-15s: %(message)s",
            level=logging.DEBUG if self._config.debug else logging.INFO,
        )
        return logging.getLogger('valuesets_data')
    

    def load_data(self) -> None:
        data = self.fetch_vs_data_from_json(self._config.json_url)
        self._load_data_into_cache(data)


    def _load_data_into_cache(self, vs_data_raw: dict) -> None:
        """Loads data fetched from JSON into memory Pandas DataFrame"""

        self._logger.info("Loading in-memory cache")
        if not vs_data_raw:
            self._logger.error('Something went wrong with loading the ValueSets')
            raise Exception('Something went wrong with loading the ValueSets')
        
        def make_row(key: str, vals: tuple[str]) -> tuple[str]:
            rr = [key,]
            rr.extend(vals)
            return tuple(rr)
        
        values = [ make_row(k,v) for k,v in vs_data_raw.items() ]

        col_names = [
            'accession_id',
            'label',
            'value',
            'is_current',
            'definition',
            'description'
        ]
        self._data = pd.DataFrame(values,index=vs_data_raw.keys(), columns=col_names)
        self._data['is_current'] = self._data['is_current'].replace([0,1],[False, True])


    def fetch_vs_data_from_json(self, url: ParseResult = None) -> dict[str,tuple[str]]:
        """Fetch ValueSets from external JSON file"""
        if not url:
            url = self._config.json_url
        if url.scheme not in ('file', 'http', 'https'):
            self._logger.error('Invalid scheme for valuesets URL; must be "file", "http", "https"')
            raise ValueError('Invalid scheme for valuesets URL; must be "file", "http", "https"')

        vs_data = {}
        if url.scheme == 'file':
            self._logger.info('Loading JSON from file URL: %s', url.geturl())
            filename = Path(url.netloc) / Path(url.path)
            if not filename.exists() or not filename.is_file():
                self._logger.error('Provided input filename %s does not exists or is not a file', url)
                raise ValueError(f'Provided input filename {url} does not exists or is not a file')
            with open(filename, 'rt') as fh:
                vs_data = json.load(fh)
        else:
            self._logger.info('Loading JSON from http(s) URL: %s', url.geturl())
            r = requests.get(url.geturl(), headers={ "Content-Type" : "application/json"}, timeout=self._config.request_timeout)
            if not r.ok:
                self._logger.error('Request failed with code %s', r.status_code)
                r.raise_for_status()
            vs_data = r.json()

        return vs_data
    
    def get_vsdata_by_accession_id(self, accession_id: str) -> namedtuple:
        accession_id.lower()
        self._logger.debug("Getting ValueSet data by accession %s", accession_id)
        # row = self._data[self._data["accession_id"] == accession_id]
        vs = self._data.loc[self._data["accession_id"] == accession_id]
        res = tuple(vs.itertuples(name='ValueSet', index=False))
        return res[0] if res else ()


    def get_vsdata_by_value(self, value: str, is_current: bool = False) -> tuple[namedtuple]:
        value.lower()
        curr_s = 'current' if is_current else ''
        self._logger.debug("Getting %s ValueSet data by value %s", curr_s, value)
        if is_current:
            vs = self._data.loc[(self._data["value"] == value) & (self._data["is_current"] == is_current)]
        else:
            vs = self._data.loc[self._data["value"] == value]
        res = tuple(vs.itertuples(name='ValueSet', index=False))
        return res if res else ()


    def get_vsdata_by_domain(self, domain: str, is_current: bool = False) -> tuple[namedtuple]:
        domain.lower()
        curr_s = 'current' if is_current else ''
        self._logger.debug("Getting %s ValueSet data by domain %s", curr_s, domain)
        if is_current:
            vs = self._data.loc[
                (self._data["accession_id"].str.contains(domain)) 
                & (self._data["is_current"] == is_current)
            ]
        else:
            vs = self._data.loc[self._data["accession_id"].str.contains(domain)]
        res = tuple(vs.itertuples(name='ValueSet', index=False))
        return res if res else ()

    def get_all(self, is_current: bool = False) -> tuple[namedtuple]:
        curr_s = 'current' if is_current else ''
        self._logger.debug("Getting all %s ValueSet data", curr_s)
        if is_current:
            vs = self._data.loc[self._data["is_current"] == is_current]
        else:
            vs = self._data
        res = tuple(vs.itertuples(name='ValueSet', index=False))
        return res if res else ()


# def main(logger = None, config: Config = default_conf):
#     vs_data = ValueSetData(autoload=True)
#     # data = vs_data.fetch_vs_data_from_json()
#     # for k,v in data.items():
#     #     print(f'{k}: {v}')
#     # vset_d = vs_data.get_vsdata_by_accession_id('mane.select')
#     vset_ds = vs_data.get_vsdata_by_value('select')
#     # print(vset_d)
#     # vset_ds = vs_data.get_vsdata_by_domain('mane')
#     # vset_ds = vs_data.get_all()
#     for item in vset_ds:
#         print(item)


# if __name__ == '__main__':
#     main()