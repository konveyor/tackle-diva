#	Copyright IBM Corporation 2021
#	
#	Licensed under the Eclipse Public License 2.0, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

import json
import sys
from sqlparse import sqlexp

json_open = open(sys.argv[1], 'r')
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
                            for str in sql:
                                if ':from' in str:
                                    elements = str[':from']

                                    if type(elements[0]) is unicode:
                                        db_list.append(elements[0])

db_dict[sys.argv[2]] = list(set(db_list))
print json.dumps(db_dict, indent=2)