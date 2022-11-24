
from __future__ import print_function


import json
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from collections import OrderedDict

from sqlparse import sqlexp

def get_opts(argv=['']):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input', nargs='?', default='transaction.json', help='DiVA transaction json file')
    p.add_argument('-s', '--server', default='localhost', help='neo4j server hostname')
    p.add_argument('-p', '--port', default='7687', help='neo4j server portnumber')
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
        ts = [ list(t.values())[0] if isinstance(t, dict) else t for t in ast[':from'] if not isinstance(t, tuple)]
        res = set()
        for t in ts:
            if isinstance(t, list):
                res |= crud0(t, False)[0]
            else:
                res.add(t)
        return [set(), res] if write else [res, set()]
    else:
        return [set(), set()]

def crud(sql):
    r = sqlexp(sql.lower())
    if r:
        return crud0(r[1])
    else:
        return [set(), set()]

def analyze(txs, opts):
    for tx in txs:
        stack = []
        if tx['transaction'] and tx['transaction'][0]['sql'] != 'BEGIN':
            tx['transaction'] = [{ 'sql': 'BEGIN' }] + tx['transaction']
        for op in tx['transaction']:
            if op['sql'] == 'BEGIN':
                stack.append([set(), set()])
                op['rwset'] = stack[-1]
            elif op['sql'] in ('COMMIT', 'ROLLBACK'):
                if len(stack) > 1:
                    stack[-2][0] |= stack[-1][0]
                    stack[-2][1] |= stack[-1][1]
                stack[-1][0] = set(stack[-1][0])
                stack[-1][1] = set(stack[-1][1])
                stack.pop()
            else:
                rs, ws = crud(op['sql'])
                stack[-1][0] |= rs
                stack[-1][1] |= ws
    return txs

def neo4j(txs, label, session):
    for tx in txs:
        txid = tx['txid']
        rset, wset = tx['transaction'][0]['rwset']

        for t in rset:
            #print("MERGE (a:Tx{label:'%s', txid:'%d'}) MERGE (b:Table{name:'%s'}) CREATE (a)-[:Read]->(b)" % (label, txid, t))
            session.run("MERGE (a:Tx{label:'%s', txid:'%d'}) MERGE (b:Table{name:'%s'}) CREATE (a)-[:Read]->(b)" % (label, txid, t))

        for t in wset:
            #print("MERGE (a:Tx{label:'%s', txid:'%d'}) MERGE (b:Table{name:'%s'}) CREATE (a)-[:Write]->(b)" % (label, txid, t))
            session.run("MERGE (a:Tx{label:'%s', txid:'%d'}) MERGE (b:Table{name:'%s'}) CREATE (a)-[:Write]->(b)" % (label, txid, t))


if __name__ == '__main__':
    import sys
    import yaml

    yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
    
    opts = get_opts(sys.argv[1:])

    data = json.load(open(opts.input), object_pairs_hook=OrderedDict)

    from neo4j import GraphDatabase
    driver = GraphDatabase.driver('bolt://%s:%s' % (opts.server,opts.port))
    session = driver.session()
    
    for c, entry in enumerate(data):
        res = analyze(entry['transactions'], opts)
        del(entry['transactions'])
        label = yaml.dump(entry, default_flow_style=True).strip().replace("'", "")
        neo4j(res, label, session)

    session.close()