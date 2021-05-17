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

from __future__ import print_function


import json
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


#from urlparse import urlparse, parse_qs
from collections import OrderedDict

from sqlparse import sqlexp

def get_opts(argv=['']):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input', nargs='?', default='res.json', help='input transaction file')
    # p.add_argument('-d', '--dot', action='store_true', help='graphviz output')
    return p.parse_args(argv)


def crud0(ast, write=False):
    if isinstance(ast, list):
        res = [set(), set()]
        for child in ast[1:]:
            rs, ws = crud0(child, ast[0] != 'select')
            res[0] |= rs
            res[1] |= ws
        return res
    elif isinstance(ast, dict) and ':from' in ast:
        ts = [ t.values()[0] if isinstance(t, dict) else t for t in ast[':from'] if not isinstance(t, tuple)]
        return [set(), set(ts)] if write else [set(ts), set()]
    else:
        return [set(), set()]

def crud(sql):
    r = sqlexp(sql.lower())
    if r: 
        return crud0(r[1])
    else:
        return [set(), set()]

def analyze(txs, opts):
    # annotate subtransaction, e.g., BEGIN? by 
    # dependency relation
    # 
    # TODO: what about already parallel txs? 
    for tx in txs:
        stack = []
        for op in tx['transaction']:
            if op['sql'] == 'BEGIN':
                stack.append([set(), set()])
                op['rwset'] = stack[-1]
            elif op['sql'] in ('COMMIT', 'ROLLBACK'):
                if len(stack) > 1:
                    stack[-2][0] |= stack[-1][0]
                    stack[-2][1] |= stack[-1][1]
                stack[-1][0] = list(stack[-1][0])
                stack[-1][1] = list(stack[-1][1])
                stack.pop()
            else:
                #s = op['callgraph'][-1]
                #s = s[s.rindex('@'):]
                rs, ws = crud(op['sql'])
                #stack[-1][0] |= set([t + s for t in rs])
                #stack[-1][1] |= set([t + s for t in ws])
                stack[-1][0] |= rs
                stack[-1][1] |= ws
    return txs

def trancl(edges):
    # transitive closure
    cont = True
    while cont:
        cont = False
        for i in edges:
            for j in list(edges[i]):
                for k in edges.get(j, set()) - edges[i]:
                    edges[i].add(k)
                    cont = True
    return edges

def tranred(edges):
    # transitive reduction
    trancl(edges)
    dups = {}
    for i in edges:
        for j in edges[i]:
            for k in edges.get(j, []):
                dups.setdefault(i, set()).add(k)
    for i in edges:
        edges[i] -= dups.get(i, set())
    return edges

def dump_dot(c, label, txs, opts):


    print('subgraph cluster_%d {' % c)
    print('label="%s"' % label)
    i = 0
    text = ''

    rwsets = {}
    
    for tx in txs:
        stack = []
        for op in tx['transaction']:

            sql = op['sql']
            if op['sql'] == 'BEGIN':
                if not stack:
                    rwsets[i] = op['rwset']
                stack.append(None)
                sql += ' ' + json.dumps({'rwset' : map(list, op['rwset'])}).replace('"', '')

            text += '<tr><td align="text">%s<br align="left" /></td></tr>' % ('  ' *len(stack) + sql) 

            if op['sql'] in ('COMMIT', 'ROLLBACK'):
                stack.pop()
                if not stack:
                    print ('n%i_%i [label=<<table border="0">%s</table>>]' % (c, i, text))
                    i += 1
                    text = ''

    edges = {}

    # print (json.dumps(rwsets, indent=2))
    for i in rwsets:
        if i == 0:
            continue
        for j in range(i):
            # print (i, j, set(rwsets[j][1]), set(rwsets[i][0]))
            if (set(rwsets[j][1]) & set(rwsets[i][0] + rwsets[i][1])
                or set(rwsets[i][1]) & set(rwsets[j][0] + rwsets[j][1])):
                edges.setdefault(j, set()).add(i)

    tranred(edges)
    for i in edges:
        for j in edges[i]:
            print('n%d_%d -> n%d_%d' % (c,i, c,j))

    print('}')
    


if __name__ == '__main__':
    import sys
    import yaml

    yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
    yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))

    opts = get_opts(sys.argv[1:])

    data = json.load(open(opts.input), object_pairs_hook=OrderedDict)

    print('digraph {')
    print('node[shape=plaintext];')
    
    for c, entry in enumerate(data):
        res = analyze(entry['transactions'], opts)
        del(entry['transactions'])
        label = yaml.dump(entry, default_flow_style=True).strip()
        dump_dot(c, label, res, opts)
        
    print('}')



    

