#	Copyright IBM Corporation 2021
#
#	Licensed under the Apache Public License 2.0, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

import json
import sys

from .sqlparse import sqlexp


def main(in_file: str, app_path: str, out_file: str = None) -> None:
    with open(in_file, 'r') as json_open:
        tx_entries = json.load(json_open)

    db_dict = {}
    db_list = []

    for tx_entry in tx_entries:
        if len(tx_entry["transactions"]) >= 1:
            for txs in tx_entry["transactions"]:
                if 'transaction' in txs:
                    for trans in txs['transaction']:
                        if 'sql' in trans:
                            sql_str = sqlexp(trans['sql'].lower())
                            if sql_str:
                                sql = sql_str[1]
                                for str_ in sql:
                                    if ':from' in str_:
                                        elements = str_[':from']

                                        if isinstance(elements[0], str):
                                            db_list.append(elements[0])

    db_dict[app_path] = list(set(db_list))
    with open(out_file, 'w') as out_fp:
        print(json.dump(db_dict, out_fp, indent=2))


if __name__ == '__main__':
    extract(in_file=sys.argv[1], app_path=sys.argv[2])
