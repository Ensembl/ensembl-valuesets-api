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

"""Configuration module"""

import os
from urllib.parse import ParseResult, urlparse
from dataclasses import dataclass

__all__ = [ 'Config', 'default_conf' , 'parse_debug_var' ]

def parse_debug_var(var: str):
    return not ((var.lower() in ("f", "false", "no", "none")) or (not var))


@dataclass
class Config():
    debug: bool
    server_port: int
    vset_source: str
    max_workers: int
    stop_timeout: int
    request_timeout: int
    json_url: ParseResult


default_conf = Config(
    debug=parse_debug_var(os.getenv("DEBUG", "false")),
    server_port=int(os.getenv("SERVER_PORT", "50051")),
    vset_source=os.getenv("VSET_JSON_URL", ""),
    max_workers=int(os.getenv("MAX_WORKERS", "10")),
    stop_timeout=int(os.getenv("STOP_TIMEOUT", "30")),
    request_timeout=int(os.getenv("REQUEST_TIMEOUT", "10")),
    json_url=urlparse('https://raw.githubusercontent.com/sgiorgetti/test-valuesets/main/valuesets.json')
)
