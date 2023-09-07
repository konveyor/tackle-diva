import types, sys, importlib


def get_opts(argv=[]):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--inplace', nargs='?', const='src/main/java/com/ibm/research/crudgen/util/SqlParse.java',
                   help='inplace replace of SqlParse.java')
    return p.parse_args(argv)

ops = []
keys = set()

def name(v, m):
    if type(v) is types.FunctionType:

        # print(v, v.__code__, dir(v.__code__), file=sys.stderr)

        for k in m:
            if m[k] is v:
                if k in ('name', 'variable0', 'literal', 'nil', ):
                    return 'SqlParse::%s' % k
                elif k not in keys:
                    return "(t,s)->SqlParse.%s.eval(t,s)" % k
                else:
                    return k
        if v.__name__ not in ('<lambda>'):
            ops.append(v)
            return v.__name__
        if v.__code__.co_argcount != 1:
            return '@'
        if v.__code__.co_names and v.__code__.co_names[0] not in ('join', 'name', '__name__', 'matching',):
            k = v.__code__.co_names[0]
            if k not in keys:
                return "(t,s)->SqlParse.%s.eval(t,s)" % k
            else:
                return k
        return name(v(m), m)
    return str(v)

def matching(n, f):
    m = str(f([],''))
    print (m, file=sys.stderr)
    # String
    if m == "['']":
        return 'match(%s, (r, v) -> new Object[] { getToken(v) })' % n
    # Field name
    elif m == "[('',)]":
        return 'match(%s, (r, v) -> new Object[] { new Field(v) })' % n
    # Scope
    elif m == "[[]]":
        return 'match(%s, (r, v) -> new Object[] { r })' % n
    elif m == "[{':from': []}]":
        return 'match(%s, (r, v) -> new Object[] { new From(r) })' % n
    # Alias (ascxt)
    elif m == "[{None: ''}]":
         return 'match(%s, (r, v) -> new Object[] { new Alias(v) })' % n
    # Env (ascxt)
    elif str(f([('',), {None: '?'}], '')) == "[{'?': ('',)}]":
        return 'match(%s, (r, v) -> getEnv(r))' % n
    # Env (colexp1)
    elif str(f([('a.b',)], '')) == "[{'b': ('a.b',)}]":
        return 'match(%s, (r, v) -> getEnv(r))' % n
    else:
        print(str(f([('a.b',)], '')), file=sys.stderr)
    return n

def process(opts=None):
    peg = types.ModuleType('peg', '')
    sys.modules['peg'] = peg

    # runs with python2 only


    peg.__dict__['seq'] = lambda *args: lambda m : 'seq(' + ','.join(name(v, m) for v in args) + ')'
    peg.__dict__['choice'] = lambda *args: lambda m : 'choice(' + ','.join(name(v, m) for v in args) + ')'
    peg.__dict__['val'] = lambda *args: lambda m : 'val(' + ','.join(name(v, m) for v in args) + ')'
    peg.__dict__['before'] = lambda *args: lambda m : 'before(' + ','.join(name(v, m) for v in args) + ')'
    peg.__dict__['star'] = lambda *args: lambda m : 'star(' + ','.join(name(v, m) for v in args) + ')'
    peg.__dict__['match'] = lambda v, f: lambda m : matching(name(v, m), f)
    peg.__dict__['nil'] = lambda m: 'nil'

    peg.__dict__['pegop'] = lambda f : lambda *args : lambda m : f.__name__ + '(' + ','.join('"' + name(v, m) + '"' if v else "(String) null" for v in args) + ')'
    peg.__dict__['pegcxt'] = lambda f : lambda v : lambda m : f.__name__ + '(' + name(v, m) + ')'

    import sqlparse

    ks = list(sqlparse.__dict__.keys())
    vs = [v.split(' ')[0] for v in open(sqlparse.__file__[:-1] if sqlparse.__file__.endswith('.pyc') else sqlparse.__file__) if ' ' in v and v[0] != ' ']

    # print(vs, file=sys.stderr)
    ks.sort(key = lambda k : vs.index(k) if k in vs else 9999)


    ignore = (
        'seq', 'token1', 'token0', 'before', 'ascxt', 'val', 'comma_sep', '__package__', 'frmcxt', 'split',
        'until_ignoring_paren', 'literal', 'pegcxt', '__doc__', 'match', 'star', 'option', 'nil', '__builtins__',
        '__file__', 'choice', 'variable0', '__name__', 'pegop', 'name', 'until', 'token', 'plus', 'op', 'match0',
    )

    res = []

    sqlparse.__dict__['colexp1'](sqlparse.__dict__)

    
    for k in ks:
        if k in ignore:
            continue
        if type(sqlparse.__dict__[k]) in (list, tuple, set):
            res.append("public static final Set<String> %s = new LinkedHashSet<>(Arrays.asList(new String[] { %s }));" % (k, ','.join('"%s"' % v for v in sqlparse.__dict__[k])))
            continue
        try:
            v = sqlparse.__dict__[k](sqlparse.__dict__)
            if type(v) is not str:
                raise
            res.append("public static final PegOp %s = %s;" %  (k, v))
        except:
            try:
                # TODO: remove nestedexp from keys
                v = sqlparse.__dict__[k].__closure__[0].cell_contents(lambda m : 'e', '(t,s)->fix[0].eval(t,s)')(sqlparse.__dict__)
                res.append("public static PegOp %s (PegOp e) { PegOp[] fix = new PegOp[] { null }; fix[0] = %s; return fix[0]; }" % (k , v))
            except:
                print (k + ": failed", file=sys.stderr)
        keys.add(k)

    return res


if __name__ == '__main__':
    import json, sys, os

    opts = get_opts(sys.argv[1:])
    res = process(opts)

    if not opts.inplace:
        for line in res:
            print (line)

    elif os.path.exists(opts.inplace):
        code = [line for line in open(opts.inplace)]

        s = [i for i in range(len(code)) if 'auto-generated code starts' in code[i]][0]
        t = [i for i in range(len(code)) if 'auto-generated code ends' in code[i]][0]

        code = code[:s+1] + ['\n'] + res + ['\n'] + code[t:]

        with open(opts.inplace, 'w') as f:
             f.writelines([line + '\n' if line and line[-1] != '\n' else line for line in code])

    else:
        print ("the file %s not found" % opts.inplace, file=sys.stderr)
