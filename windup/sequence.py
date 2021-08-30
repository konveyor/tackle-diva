import sys

description = """
Prerequisites:
$ pip3 install gremlinpython
"""

def get_opts(argv=[]):
    import argparse
    p = argparse.ArgumentParser(epilog=description, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('host', nargs='?', default='localhost', help='gremlin server host')
    return p.parse_args(argv)

def wrapline(sql):
    res = ''
    while len(sql) > 60:
        i = sql.find(' ', 60)
        if i < 0:
            break
        res += sql[:i] + ' <br> '
        sql = sql[i+1:]
    return res + sql

def getapp(g, r, ps):
    app = g.V(r).in_('contexts').next()
    for k, p in enumerate(ps):
        if app == p:
            break
    else:
        k = len(ps)
        ps.append(app)
        print ('participant P{} as {}'.format(k, g.V(app).name.next()))
    return k

def translate(g, k, r, ps):
    for tx in g.V(r).out('transactions').order().by('txid'):
        print ('activate P{}'.format(k))
        for op in g.V(tx).out('transaction').order().by('ordinal'):
            d = g.V(op).valueMap().next()
            if 'DivaSqlOpModel' in d['w:winduptype']:
                print ('P{}->>P{}: {}'.format(k, k, wrapline(d['sql'][0])))

            elif 'DivaRestCallOpModel' in d['w:winduptype']:
                es = g.V(op).out('endpointMethod').toList()
                if es:
                    r2 = g.V(es[0]).in_('constraints').next()
                    k2 = getapp(g, r2, ps)
                    print ('P{}->>P{}: {}'.format(k, k2, g.V(op).out('method').methodName.next()))
                    translate(g, k2, r2, ps)
                    print ('P{}->>P{}: '.format(k2, k))
                else:
                    print ('P{}->>P{}: {}'.format(k, k, g.V(op).out('method').methodName.next()))
        print ('deactivate P{}'.format(k))


def proc(opts):
    connection = DriverRemoteConnection('ws://{}:8182/gremlin'.format(opts.host), 'g')
    try:
        g = traversal().withRemote(connection)

        roots = g.V().has('w:winduptype', 'DivaContextModel').not_(__.out('constraints').in_('endpointMethod')).toList()

        for app in g.V().has('w:winduptype', 'DivaAppModel'):
            rs = g.V(roots).filter(__.in_('contexts').is_(app)).toList()
            if not rs:
                continue

            for r in rs:
                print ('### {}@{}'.format(g.V(r).out('constraints').methodName.next(), g.V(app).endpointName.next()))
                print ('```mermaid')
                print ('sequenceDiagram')
                ps = []
                translate(g, getapp(g, r, ps), r, ps)
                print ('```')
    finally:
        connection.close()

if __name__ == '__main__':
    opts = get_opts(sys.argv[1:])

    import json
    from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
    from gremlin_python.process.anonymous_traversal import traversal
    from gremlin_python.process.graph_traversal import __
    proc(opts)







