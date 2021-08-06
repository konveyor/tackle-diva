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
import os

file_list = os.listdir(sys.argv[1])

csv_file_name = sys.argv[1].replace('/','').replace('.','') + '.csv'
print(csv_file_name)
csv_fd = open(csv_file_name,'w')

if 'database.json' in file_list:
    with open(sys.argv[1] + '/database.json', 'r') as f:
        db_dict = json.load(f)
        csv_fd.write('database\n')
        for db in db_dict['/app']:
            print(db)
            csv_fd.write(', %s \n' % db)

if 'transaction.json' in file_list:
    with open(sys.argv[1] + '/transaction.json', 'r') as f:
        tx_dict = json.load(f)
        csv_fd.write('transactions\n')
        
        tx_entry_list = []
        for tx in tx_dict:
            tx_entry_list.append(tx['entry']['methods'][0])

        unique_tx_entry = set(tx_entry_list)
        unique_tx_entry_list = list(unique_tx_entry)
        for entry in unique_tx_entry_list:
            print(entry)
            csv_fd.write(', %s \n' % entry)

csv_fd.close()