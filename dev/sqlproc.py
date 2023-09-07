from sqlparse import sqlexp, split
import sys
import json

from collections import OrderedDict

from sortedcontainers import SortedSet as sortedset, SortedDict as sorteddict

def get_opts(argv=['']):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--crud', action='store_true', help='outputs crud csv')
    p.add_argument('-i', '--info', type=str, default=None, help='outputs information flow json for a given attribute')
    p.add_argument('-d', '--dot', action='store_true', help='outputs information flow graph')
    p.add_argument('-t', '--transaction', type=str, default=None, help='transaction json')
    p.add_argument('-m', '--mapping', type=str, default=None, help='table-column mapping json')
    return p.parse_args(argv)

def cxt(a, c0=None, opts=None):
    c = { '' : (sortedset(), {})}
    has_from = False
    for w in a:
        if not isinstance(w, dict) or ':from' not in w:
            continue
        has_from = True
        for v in w[':from']:            
            if isinstance(v, str):
                if v not in ('select', 'update', 'insert', 'delete'):
                    c.setdefault(v, (sortedset(), {}))[0].add(v)
            elif isinstance(v, dict):
                k = list(v.keys())[0]
                t = v[k]
                if isinstance(t, str):
                    c.setdefault(k, (sortedset(), {}))[0].add(t)
                elif isinstance(t, list):
                    c2 = cxt(t, opts=opts)
                    c.setdefault(k, (sortedset(), {}))
                    c[k][0].update(c2[''][0])
                    c[k][1].update(c2[''][1])
            elif isinstance(v, list):
                # TODO:
                # This detects ambiguity of "select t.a from (select * from x t union select * from y t)",
                # but not "select a from (select a from x union select a from y)".
                c2 = cxt(v, opts=opts)
                for k in c2:
                    c.setdefault(k, (sortedset(), {}))
                    c[k][0].update(c2[k][0])
                    c[k][1].update(c2[k][1])

    for k in c.keys():
        c[''][0].update(c[k][0])
        c[''][1].update(c[k][1])

    if opts.mapping:
        for k in c.keys():
            for t in c[k][0]:
                if t not in opts.mapping:
                    continue
                for col in opts.mapping[t]:
                    c[k][1][col] = (t, col)

    for v in a:
        if isinstance(v, dict):
            n = list(v.keys())[0]
            t = v[n]
            if isinstance(t, tuple):
                k, col = split(t[0])
                if col == '?':
                    continue
                if k in c and col in c[k][1]:
                    c[''][1][n] = c[k][1][col]
                elif k in c and col not in c[k][1] and len(c[k][0]) == 1:
                    c[''][1][n] = (c[k][0][0], col)
                elif col == '*' and k in c:
                    c[''][1][n] = (list(c[k][0]), col)
                else:
                    c[''][1][n] = ({ '???' : list(c[k][0]) if k in c else []}, col)
            elif isinstance(t, list):
                c[''][1][n] = None

    if c0:
        # import from the outer context, c0
        #
        for k in c0:
            # "select * from s where x in (select * from t where a = b)"
            # may be ambigous...
            #if k == '' and has_from:
            #    continue
            #
            if k in c and k != '':
                continue
            if k not in c:
                c[k] = sortedset(), {}
            c[k][0].update(c0[k][0])
            for n in c0[k][1]:
                c[k][1].setdefault(n, c0[k][1][n])
    return c

def flatten(i):
    for j in i:
        for k in j:
            yield k

def prod(*i):
    if not i:
        yield ()
    else:
        for m in prod(*i[1:]):
            for k in i[0]:
                yield (k,) + m

def resolve(a, c=None, opts=None):
    c = cxt(a, c, opts)
    r = []
    for v in flatten(v.values() if isinstance(v, dict) else [v] for v in a):
        if isinstance(v, list):
            r += [resolve(v, c, opts)]
        elif isinstance(v, tuple):
            if v[0] == 'rownum':
                continue
            if var(v):
                continue
            k, col = split(v[0])
            if col == '?':
                continue
            if k in c and col in c[k][1]:
                r += [c[k][1][col]]
            elif k in c and col not in c[k][1] and len(c[k][0]) == 1:
                r += [(c[k][0][0], col)]
            elif col == '*' and k in c:
                r += [(list(c[k][0]), col)]
            else:
                r += [({ '???' : list(c[k][0]) if k in c else []}, col)]
        elif isinstance(v, str):
            r += [v]
    return r


def calc_mapping(m, r):
    todo = [r]
    while todo:
        v = todo.pop()
        if isinstance(v, tuple) and isinstance(v[0], str) and v[1] != '*' and (v[0] not in m or v[1] not in m[v[0]]):
            m.setdefault(v[0], []).append(v[1])
        elif isinstance(v, list):
            todo += v

def calc_crud(r, op='R', opts=None):
    res = sorteddict()
    if not r:
        return res
    if isinstance(r, list):
        if r[0] == 'update':
            res = calc_crud(r[1], op='U', opts=opts)
            todo = r[2:]
        elif r[0] == 'insert':
            res = calc_crud(r[1], op='C', opts=opts)
            todo = r[2:]
        elif r[0] == 'delete':
            res = calc_crud(r[1], op='D', opts=opts)
            todo = r[2:]
        elif r[0] == 'select':
            todo = r[1:]
        else:
            todo = list(r)
        todo.reverse()
    else:
        todo = [r]
    while todo:
        v = todo.pop()
        if isinstance(v, str) and op == 'D':
            cols = [v + '.' + c for c in opts.mapping[v]]
            for col in cols:
                res[col] = ''.join(c for c in 'CRUD' if c == op or c in res.get(col, ''))
        elif isinstance(v, tuple):
            if v[1] == '*':
                if isinstance(v[0], list):
                    cols = sum([[t + '.' + c for c in opts.mapping[t]] for t in v[0]], [])
                else:
                    cols = [v[0] + '.' + c for c in opts.mapping[v[0]]]
                for col in cols:
                    res[col] = ''.join(c for c in 'CRUD' if c == op or c in res.get(col, ''))
            elif isinstance(v[0], dict):
                pass
            else:
                col = v[0] + '.' + v[1]
                # print (type(op), file=sys.stderr)
                res[col] = ''.join(c for c in 'CRUD' if c == op or c in res.get(col, ''))
        elif isinstance(v, list):
            if op in ('C', 'D'):
                for col, acc in calc_crud(v, op='R', opts=opts).items():
                    res[col] = ''.join(c for c in 'CRUD' if c in acc or c in res.get(col, ''))
            elif op == 'U':
                for col, acc in calc_crud(v[0], op='U', opts=opts).items():
                    res[col] = ''.join(c for c in 'CRUD' if c in acc or c in res.get(col, ''))
                for col, acc in calc_crud(v[1:], op='R', opts=opts).items():
                    res[col] = ''.join(c for c in 'CRUD' if c in acc or c in res.get(col, ''))
            else:
                v.reverse()
                todo += v
    return res

def proc_crud(opts=None):

    crud = []
    cols = sortedset()

    for tx in flatten(txs['transactions'] for tx in opts.transaction):
        ts = tx['transaction']
        del(tx['transaction'])
        s, i = '{', ''
        for k in tx:
            v = tx[k]
            if isinstance(v, list):
                v = '[' + ' ,'.join(v) + ']'
            s, i = s + i + k + ': ' + str(v), ', '
        s += '}'

        res = sorteddict()
        for e in ts:
            if 'sql' not in e or not e['sql']:
                continue

            sql = e['sql'].lower()

            while '/*' in sql:
                sql = sql[:sql.index('/*')] + sql[sql.index('*/') + 2:]

            sql = sql.strip()
            # print (sql, file=sys.stderr)

            a = sqlexp(sql)
            if not a:
                print ("parse failed: " + sql, file=sys.stderr)
                continue
            r = resolve(a[1], opts=opts)
            if '???' in str(r):
                print (sql, a[1], r, file=sys.stderr)

            for col, acc in calc_crud(r, opts=opts).items():
                res[col] = ''.join(c for c in 'CRUD' if c in acc or c in res.get(col, ''))

        cols.update(res.keys())
        crud.append((s, res))

    cols = list(cols)
    print (','.join([''] + cols))
    for s, res in crud:
        print(','.join(['"%s"' % s] + [res.get(c, '') for c in cols]))


def rename(a, cnt=[1]):
    if isinstance(a, tuple):
        if a[0] == '?':
            a = ('?{}'.format(cnt[0]),)
            cnt[0] += 1
    elif isinstance(a, list):
        for i, a0 in enumerate(a):
            a[i] = rename(a0, cnt)
    elif isinstance(a, dict):
        for k in a:
            a[k] = rename(a[k], cnt)
    return a


def var(a):
    if not isinstance(a, tuple):
        return None
    s = a[0]
    if s and s[0] == '?':
        return s[1:]
    elif s and s[0] == '#' and s[1] == '{':
        return s[2: s.rindex(',') if ',' in s else s.rindex('}')]
    return None

def resolve_args(a, c=None, opts=None, res=None):
    if not res:
        res = {}
        a = rename(a)
    c = cxt(a, c, opts)
    if not a:
        return res
    if a[0] == 'insert':
        fs = resolve(a[1][':from'], c, opts)
        for k, f in enumerate(fs[1:]):
            if 'values' in a:
                for s in a[3 + k]:
                    if var(s):
                        res[var(s)] = f[0] + '.' + f[1]
    elif a[0] == 'update':
        for w in a[1][':from'][1:]:
            f = resolve(w[:1], c, opts)[0]
            for s in w[1:]:
                if var(s):
                    res[var(s)] = f[0] + '.' + f[1]
    else:
        for v in flatten(v.values() if isinstance(v, dict) else [v] for v in a):
            if isinstance(v, list) and v:
                resolve_args(v, c, opts, res)
    return res

def proc_tx(opts=None):
    m = {}

    for tx in flatten(txs['transactions'] for txs in opts.transaction):
        for e in tx['transaction']:
            if 'sql' not in e or not e['sql']:
                continue

            sql = e['sql'].lower()

            while '/*' in sql:
                sql = sql[:sql.index('/*')] + sql[sql.index('*/') + 2:]

            sql = sql.strip()

            a = sqlexp(sql)
            if not a:
                print ("parse failed: " + sql, file=sys.stderr)
                continue

            ps = resolve_args(a[1], opts=opts)

            if 0 and 'infoflow' in e:
                ifw = sorteddict()
                for k in e['infoflow']:
                    if k.startswith('arg:'):
                        n = k[len('arg:'):].lower()
                        if n in ps:
                            ifw['attr:' + ps[n]] = e['infoflow'][k]
                        else:
                            ifw[k] = e['infoflow'][k]
                    else:
                        ifw[k] = e['infoflow'][k]
                e['infoflow'] = ifw
            else:
                e['args'] = ps

            r = resolve(a[1], opts=opts)
            if '???' in str(r):
                print (sql, a[1], r, file=sys.stderr)

            calc_mapping(m, r)

            # print (r, m, file=sys.stderr)

            if r[0] == 'select' and opts.mapping:
                res = sorteddict()
                for f in r[1:]:
                    if not f or isinstance(f, list):
                        break
                    for f0 in [(t0, f[1]) for t0 in f[0]] if isinstance(f[0], list) else [f]:
                        if isinstance(f0[0], dict):
                            pass
                        elif f0[1] == '*':
                            for a in opts.mapping[f0[0]]:
                                res[a] = 'attr:' + f0[0] + '.' + a
                        else:
                            res[f0[1]] = 'attr:' + f0[0] + '.' + f0[1]
                e['result'] = res

            if opts.mapping:
                e['crud'] = OrderedDict(calc_crud(r, opts=opts))
            else:
                e['parsed'] = r

    if opts.info:
        filter_info(opts)

    if not opts.mapping:
        json.dump(m, open('mapping.json', 'w'), indent=2)


def filter_info(opts=None):
    res = []
    attr = 'attr:' + opts.info
    for txs in opts.transaction:
        fs = sortedset()
        rs = sortedset()
        for op in flatten(tx['transaction'] for tx in txs['transactions']):
            if opts.info in op.get('crud', {}):
                crud = op.get('crud', {})[opts.info]
                if 'U' in crud or 'C' in crud:
                    fs.add(op['opid'])
                    if attr in op.get('infoflow', {}):
                        for v in op.get('infoflow', {})[attr]:
                            if v.startswith('sqlop:'):
                                op2 = int(v[6:v.index('.')])
                                fs.add(op2)
                for k, v in op.get('result', {}).items():
                    if v == attr:
                        rs.add((op['opid'], k))
                        rs.add((op['opid'], '*'))
            else:
                for v in flatten(op.get('infoflow', {}).values()):
                    if v.startswith('sqlop:'):
                        op2 = int(v[6:v.index('.')])
                        k = v[v.index('.')+1:]
                        if (op2, k.lower()) in rs:
                            fs.add(op['opid'])
                            fs.add(op2)
        txs2 = []
        for tx in txs['transactions']:
            tx2 = []
            for op in tx['transaction']:
                if op['opid'] in fs:
                    tx2.append(op)
            if tx2:
                tx['transaction'] = tx2
                txs2.append(tx)
        if txs2:
            txs['transactions'] = txs2
            res.append(txs)

    opts.transaction = res


def gen_dot(opts):
    print ('digraph {')
    print ('node[shape=plaintext];')
    print ('rankdir=LR;')
    cid = 0
    tbls = sorteddict()

    edges = []
    
    for txs in opts.transaction:
        act = txs['dispatch'].values().__iter__().__next__()[0]
        act = act[act.rindex('/')+1:]
        print ('subgraph cluster_{} {{'.format(cid))
        print ('label="{}"'.format(act))

        params = sortedset()
        ops = sorteddict()
        for op in flatten(tx['transaction'] for tx in txs['transactions']):
            for v in flatten(op.get('infoflow',{}).values()):
                if v.startswith('http-param:'):
                    params.add(v[len('http-param:'):])
                if v.startswith('sqlop:'):
                    id, a = v[len('sqlop:'):].split('.')
                    if int(id) not in ops:
                        ops[int(id)] = sortedset()
                    ops[int(id)].add(a)
            for v in op.get('args', {}).values():
                t, a = v.split('.')
                if t not in tbls:
                    tbls[t] = sortedset()
                tbls[t].add(a)
            for v in op.get('result', {}).values():
                if v.startswith('attr:'):
                    t, a = v[len('attr:'):].split('.')
                    if t not in tbls:
                        tbls[t] = sortedset()
                    tbls[t].add(a)

        pid = 0
        if params:
            print ('subgraph cluster_{}_{} {{'.format(cid, pid))
            print ('label="http-param"')
            for k, v in enumerate(params):
                print ('n{}_{}_{} [label="{}"]'.format(cid, pid, k, v))
            pid += 1
            print ('}')
            
        for op in flatten(tx['transaction'] for tx in txs['transactions']):
            print ('subgraph cluster_{}_{} {{'.format(cid, pid))
            if 'sql' in op and 0:
                print ('label="opid={} sql={}"'.format(op['opid'], op['sql']))
            else:
                print ('label="opid={}"'.format(op['opid']))
            if op['opid'] in ops and '*' in ops[op['opid']]:
                print ('n{}_{}__ [label="{}"]'.format(cid, op['opid'], '*'))
                

            args = sortedset()
            for k in op.get('infoflow', []):
                args.add(k)
            for k in op.get('result', []):
                args.add(k)
            if 'infoflow' in op:
                for k in op['infoflow']:
                    print ('n{}_{}_{} [label="{}"]'.format(cid, pid, args.index(k), k))
                    v = op['infoflow'][k][0]
                    if v.startswith('http-param:'):
                        v = v[len('http-param:'):]
                        print ('n{}_{}_{} -> n{}_{}_{}'.format(cid, 0, params.index(v), cid, pid, args.index(k)))
                    if v.startswith('sqlop:'):
                        id, a = v[len('sqlop:'):].split('.')
                        if a == '*':
                            edges.append('n{}_{}__ -> n{}_{}_{}'.format(cid, id, cid, pid, args.index(k)))

                    if 'args' in op and k.startswith('arg:'):
                        v2 = op['args'].get(k[len('arg:'):].lower(), None)
                        if v2:
                            t, a = v2.split('.')
                            edges.append('n{}_{}_{} -> {}_{}'.format(cid, pid, args.index(k), t, a))
            if 'result' in op:
                for k in op['result']:
                    print ('n{}_{}_{} [label="{}"]'.format(cid, pid, args.index(k), k))
                    v = op['result'][k]
                    if v.startswith('attr:'):
                        t, a = v[len('attr:'):].split('.')
                        edges.append('{}_{} -> n{}_{}_{}'.format(t, a, cid, pid, args.index(k)))
                            
            pid += 1
            print ('}')

        cid += 1
        print ('}')

    for t in tbls:
        print ('subgraph cluster_{} {{'.format(t))
        print ('label="{}"'.format(t)) 
        for a in tbls[t]:
            print ('{}_{} [label="{}"]'.format(t, a, a))
        print ('}')

    for e in edges:
        print (e)

    print ('}')


if __name__ == '__main__':

    from collections import OrderedDict

    opts = get_opts(sys.argv[1:])

    if opts.mapping:
        opts.mapping = json.load(open(opts.mapping), object_pairs_hook=OrderedDict)

    if opts.transaction:
        opts.transaction = json.load(open(opts.transaction), object_pairs_hook=OrderedDict)

    sys.setrecursionlimit(10000)

    if opts.crud:
        if not opts.mapping:
            print('Calculate mapping.json first', file=sys.stderr)
            exit(0)
        proc_crud(opts)

    elif opts.transaction:
        proc_tx(opts)

        if not opts.dot:
            print (json.dumps(opts.transaction, indent=2))

        else:
            gen_dot(opts)
    else:
        proc_stdin(opts)
