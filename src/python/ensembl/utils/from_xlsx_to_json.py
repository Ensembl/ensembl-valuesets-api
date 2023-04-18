#!/usr/bin/env python3

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

"""from_xlsx_to_json.py script.

To be executed as __main__ it will expect an Excel workbook (XLSX) from
which to derive the ValueSets in JSON format.

The Excel workbook is assumed to contain all the ValueSet data in one sheet,
and columns such as
Accession_ID, label, value, colD(unused), colE(unused), definition, description
"""

__all__ = [ 'main' ]

from openpyxl import Workbook as wb
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

import json
from pathlib import Path

import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def read_xlsx(filename: Path, sheet_name: str = 'Master') -> dict[str,tuple]:
    """Reads data from an Excel spreadsheet (one named sheet),
    and creates a dictionary out of these.
    
    One column (accession) is supposed to be the unique identifier of
    a valueset, which is entirely described by the row in the sheet.

    Args:
        filename (Path): the path/name of the Excel file
        sheet_name (str): the name of the sheet to read from (defaults to 'Master')

    Returns:
        A dictionary, whose key is the value of the cell from the first column (accession),
        and value is a tuple comprising the other values in the same sheet's row.
    """
    if not filename or not filename.is_file():
        logging.error("Invalid filename provided - not a file or not found")
        raise ValueError(f'Invalid filename, pls check')
    logging.info("Called read_xlsx for file %s", filename)
    wb = load_workbook(filename)
    logging.debug(f"The number of worksheets is {len(wb.worksheets)}")
    logging.debug(f"Worksheet name(s): {wb.worksheets}")
    logging.debug(f"Selecting Worksheet {sheet_name}")
    wsheet = wb[f'{sheet_name}']
    logging.debug(f'Now in sheet: {wsheet.title}')

    data = {}
    for row in wsheet.rows:
        vals = [ str(c.value).strip() if c.value else '' for c in row ][0:7]
        logging.debug(f'Found row: {vals}')
        # Removing cols D and E, which are unused as of mid-Apr 2023
        del vals[3:5]
        # Remaining fields are
        # Accession_ID, label, value, definition, description
        data[vals[0]] = tuple(vals[1:])

    data.pop('Accession_ID', None)

    return data


def dump_data_to_json(data: dict, out_filename: Path = Path('out.json')):
    """Dumps dictionary data into JSON file.

    Args:
        data (dict): the valuesets definition data dictionary
        out_filename (Path): full filename for the output file (defaults to 'out.json')

    Returns:
        None
    """
    with open(out_filename, 'wt') as fh:
        json.dump(data, fh, indent=4)

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("filename", help="Input Excel workbook filename")
    parser.add_argument("-s", "--sheet", default="Master", help="Input Excel sheet (default: Master)")
    parser.add_argument("-o", "--out-filename", default="valuesets.json", help="Output JSON filename (default: out.json)")
    parser.add_argument("--log-level", default="INFO", help="Log level")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)

    if not args.filename:
        raise ValueError(f'Missing argument filename')
    
    xlsx_data = read_xlsx(Path(args.filename), args.sheet)

    dump_data_to_json(xlsx_data, args.out_filename)



if __name__ == '__main__':
    main()
