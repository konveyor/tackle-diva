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


from peg import seq, val, before, choice, star, nil, pegop, pegcxt
from peg import match as match0

def option(v):
    return choice(v, nil)

reserved = [
    'as', 'by', 'in', 'on', 'asc', 'all', 'end', 'set', 'from', 'left', 'join', 'full', 'desc',
    'case', 'when', 'then', 'else', 'into', 'where', 'group', 'inner', 'outer', 'order', 'right',
    'union', 'except', 'select', 'update', 'delete', 'insert', 'null', 'having',
    'listagg', 'within', 'current', 'fetch', 'concat', 'nextval', 'for', 'and', 'or', 'is', 'not',
    'like', 'escape', 'partition', 'exists', 'top',
    ':_where_in', ':_where_and', ':_where_or', ':_in', ':_or', ':_and',
]

# See https://www.ibm.com/support/knowledgecenter/SSEPEK_10.0.0/sqlref/src/tpc/db2z_reservedwords.html

reserved_that_can_be_names =  [
    'as', 'by', 'in', 'on', 'all', 'set', 'from', 'left', 'join', 'full', 'when', 'then', 'else',
    'where', 'group', 'inner', 'outer', 'order', 'right', 'union', 'except', 'select', 'delete', 'insert',
    'listagg', 'within', 'current', 'fetch', 'concat', 'for', 'partition',
]

what_only_follow_names = [
    ')', ',', 'as', 'in', 'on', 'where', 'then', 'else', 'inner'
]

operator_tokens = [
    '||', '<=', '>=', '<>', '!=', '(+)', '=*', '*=',
]

def token0(s):
    k0 = 0
    while k0 < len(s):
        if not s[k0].isspace():
            break
        k0 += 1
    else:
        return ()
    if k0 + 2 <= len(s) and s[k0:k0+2] in operator_tokens:
        return (s[k0+2:], [s[k0:k0+2]])
    if k0 + 3 <= len(s) and s[k0:k0+3] in operator_tokens:
        return (s[k0+3:], [s[k0:k0+3]])
    k = k0 + 1
    if s[k0].isalpha() or s[k0] == '_' or s[k0] == ':':
        while k < len(s):
            if not s[k].isalnum() and s[k] != '_':
                break
            k += 1
    elif s[k0].isdigit() or s[k0] == '.':
        p = s[k0] == '.'
        while k < len(s):
            if s[k] == '.' and p:
                break
            elif s[k] == '.':
                p = True
            elif not s[k].isdigit():
                break
            k += 1
    elif s[k0] == "'" or s[k0] == '"':
        while k < len(s):
            if s[k] == s[k0]:
                k += 1
                break
            k += 1
    return (s[k:], [s[k0:k]]) if k > k0 else ()

@pegop
def token1(s):
    r = token0(s)
    if r and r[1][0] in reserved_that_can_be_names:
        r2 = token0(r[0])
        if not r2 or r2[1][0] in what_only_follow_names:
            return (r[0], ['"%s"' % r[1][0]])
    if r and r[1][0] in reserved and r[0] and r[0][0] == '.':
        return (r[0], ['"%s"' % r[1][0]])
    return r

token = token1() # caching tokenization

def name(s):
    r = token(s)
    return (r[0], []) if r and r[1][0] not in reserved and (r[1][0][0] == '_' or r[1][0][0].isalpha() or r[1][0][0] == '"') else ()

def literal(s):
    r = token(s)
    if r and r[1][0][0] == "'":
        return (r[0], [])
    if r and r[1][0] == "null":
        return (r[0], [])
    if r and (r[1][0][0].isdigit() or r[1][0][0] == '.' and len(r[1][0]) > 1):
        return (r[0], [])
    return ()

def variable0(s):
    r = token(s)
    if r and r[1][0][0] == ":":
        return (r[0], [])
    if r and r[1][0] == "?":
        return (r[0], [])
    return ()

@pegop
def op(s, v):
    r = token(s)
    return (r[0], []) if r and r[1][0] == v else ()

@pegop
def until(s, *ws):
    while 1:
        r = token(s)
        if not r:
            return ('', []) if None in ws else ()
        if r[1][0] in ws:
            return (s, [])
        s = r[0]

def match(e, r=None):
    if r is None:
        return match0(e, lambda s, v: s + [v.strip()])
    else:
        return match0(e, lambda s, v: r(s, v.strip()))

def split(n):
    if '.' not in n:
        return ('', n)
    else:
        p = n.rindex('.')
        return (n[:p], n[p+1:])

qname = seq(name, star(seq(op('.'), name)))

variable = choice(variable0, seq(op('#'), op('{'), token, op('}')))

paren = seq(op('('), star(seq(until('(', ')'), lambda s : paren(s))), until('(', ')'), op(')'))

# skip until one of strs occurs, ignoring anything inside parenthesis
until_ignoring_paren = lambda *strs: seq(star(seq(until('(', ')', *strs), paren)), until('(', ')', *strs), until(*strs))

comma_sep = lambda e : seq(e, star(seq(op(','), e)))
plus = lambda e : seq(e, star(e))

# [{ s[-1][None] : s[0] }] if len(s) == 2 and seq(qname, option(op('as')), name)(v) == ('', []) else

ascxt = lambda e: match(seq(e, option(seq(option(op('as')), match(name, lambda s,v: [{None:v}])))),
                        lambda s, v :
                        [{ s[-1][None] : s[0] if len(s) == 2 else s[:-1] }] if s and isinstance(s[-1], dict) and None in s[-1] else
                        s)

func = choice(qname, variable, op('left'), op('right'), op('concat'))

callargs = choice(
    comma_sep(seq(
        option(choice(op('distinct'), op('all'))),
        choice(
            lambda s : colexp(s),
            match(op('*'), lambda s, v: s + [(v,)])))),
    nil)

callexp = choice(
    seq(op('listagg'), op('('), callargs, op(')'), option(seq(op('within'), op('group'), paren))),
    seq(op('cast'), op('('), lambda s: colexp(s), op('as'), until_ignoring_paren(')'), op(')')),
    seq(func, op('('), callargs, op(')'), option(seq(op('over'), paren))))

caseexp = seq(
    op('case'),
    option(lambda s : colexp(s)),
    plus(seq(op('when'), until_ignoring_paren('then'), op('then'), lambda s : colexp(s))),
    option(seq(op('else'), lambda s: colexp(s))),
    op('end'))

colexp0 = choice(
    literal,
    match(variable, lambda s, v: s + [(v,)]),
    seq(op('current'), name),
    callexp,
    caseexp,
    seq(op('('), comma_sep(lambda s : colexp(s)), op(')')),
    lambda s: nestedexp(s),
    match(seq(name, op('.'), op('*')), lambda s, v: s + [(v,)]),
    seq(option(seq(op('nextval'), op('for'))),
        match(qname, lambda s, v: s + [(v,)]),
        option(seq(op('.'), op('nextval')))),
    seq(op('set'), op('('), lambda s : colexp(s), op(')')))

binaryexp = seq(
    colexp0,
    choice(op('+'), op('-'), op('*'), op('/'), op('||'), op('concat')),
    lambda s: colexp(s))

naryexp = choice(
    seq(op('-'), lambda s: colexp(s)),
    binaryexp)

colexp = choice(naryexp, colexp0)

colexp1 = match(ascxt(colexp), lambda s, _:
                [{ split(s[0][0])[1] : s[0]}] if len(s) == 1 and isinstance(s[0], tuple) and qname(s[0][0]) == ('', [])
                else s)

#colexp1 = match(ascxt(colexp), lambda s, _:
#                [{s[1].keys()[0] : s[0] }] if len(s) > 1
#                else s)

colsexp = choice(comma_sep(colexp1), match(op('*'), lambda s, v: s + [(v,)]))

jointype = choice(
    seq(choice(op('left'), op('right'), op('full')), option(op('outer')), op('join')),
    seq(op('inner'), op('join')))

joincond = seq(op('on'), lambda s : condexp(s))

tblexp = choice(
    seq(match(qname),
        option(seq(op('partition'), op('('), name, op(')')))),
    lambda s : nestedexp(s),
    seq(op('('), lambda s : tblsexp(s), op(')')))

frmcxt = lambda e : match(e, lambda s, _ : [{':from' : s}])

tblsexp = frmcxt(seq(
    ascxt(tblexp),
    star(choice(
        seq(op(','), ascxt(tblexp)),
        seq(plus(seq(jointype, ascxt(tblexp))), joincond))),
    option(joincond)))

@pegcxt
def unioncxt(e, fix):
    return seq(
        choice(e, seq(op('('), choice(e, fix), op(')'))),
        star(seq(
            choice(
                seq(op('union'), option(op('all'))),
                op('except')),
            match(choice(e, seq(op('('), choice(e, fix), op(')'))), lambda s, v: [s]))),
        option(grpexp),
        option(orderexp))

@pegcxt
def withcxt(e, fix):
    return choice(
        seq(op('with'),
            comma_sep(seq(
                name,
                option(seq(op('('), comma_sep(name), op(')'))),
                op('as'),
                lambda s: nestedexp(s))), e),
        e)

colexp2 = choice(seq(qname, op('(+)')), colexp)

condexp = seq(choice(
    seq(op('('),
        lambda s: condexp(s),
        op(')')),
    seq(op('not'),
        lambda s : condexp(s)),
    seq(op('exists'),
        choice(colexp, lambda s: nestedexp(s))),
    seq(colexp2,
        choice(
            seq(choice(
                op('='), op('<'), op('>'), op('<='), op('>='), op('<>'), op('!='), op('*='), op('=*'),
                seq(op('is'), option(op('not')))),
                colexp2),
            seq(option(op('not')), choice(
                seq(op('in'),
                    choice(colexp, lambda s :nestedexp(s))),
                seq(op('like'),
                    colexp,
                    option(seq(op('escape'), colexp))),
                seq(op('between'),
                    colexp, op('and'), colexp))),
            variable)),
    seq(choice(op(':_where_and'), op(':_or'), op(':_and')), op('('), comma_sep(lambda s : condexp(s)), op(')')),
    seq(op(':_in'), op('('), qname, option(op('=')), variable, op(')')),
    callexp),
    option(seq(
        choice(op('and'), op('or')),
        lambda s: condexp(s))))

# whrexp = seq(op('where'), until_ignoring_paren(')', 'group', 'order', 'union', None))
whrexp = choice(
    seq(op('where'), condexp),
    seq(choice(
        seq(op(':_where_in'), colexp),
        seq(choice(op(':_where_and'), op(':_where_or')), op('('), option(condexp),
            star(seq(option(op(',')), choice(condexp, variable))), op(')'))),
        option(seq(choice(op('and'), op('or')),
                   condexp))))

havingexp = seq(op('having'), condexp)

grpexp = seq(op('group'), op('by'), comma_sep(choice(qname, variable)))
orderexp = seq(op('order'), op('by'), comma_sep(seq(colexp, option(choice(op('asc'), op('desc'))))))

assignexp = match(seq(choice(match(qname, lambda s,v: s +[(v,)]),
                       seq(op('('), comma_sep(match(qname, lambda s,v: s +[(v,)])), op(')'))),
                      op('='), colexp),
                  lambda s,v: [s])
assignsexp = seq(assignexp, star(seq(op(','), assignexp)))

frmspec = seq(
    tblsexp,
    option(whrexp),
    option(grpexp),
    option(havingexp),
    option(orderexp),
    option(variable),
    option(seq(op('fetch'), op('first'), choice(literal, variable, nil), op('rows'), op('only'))),
    option(seq(op('for'), op('update'),
               choice(op('nowait'),
                      seq(op('wait'), literal),
                      seq(op('with'), op('rs')),
                      nil))),
    option(seq(op('with'), op('ur'))))

selexp = withcxt(unioncxt(seq(match(op('select')), option(op('distinct')), option(seq(op('top'), literal)), colsexp, option(op(',')), option(seq(op('into'), colsexp)), op('from'), frmspec)))
updexp = withcxt(seq(match(op('update')), frmcxt(seq(ascxt(match(qname)), op('set'), assignsexp)), option(whrexp)))
insexp = withcxt(seq(match(op('insert')), op('into'), frmcxt(seq(ascxt(match(qname)), option(seq(op('('), comma_sep(match(qname, lambda s,v: s +[(v,)])), op(')'))))),
                     op('values'), choice(lambda s: nestedexp(s), seq(op('('), colsexp, op(')')), colsexp)))
delexp = withcxt(seq(match(op('delete')), option(op('from')), frmcxt(ascxt(match(qname))), option(whrexp)))

valuesexp = seq(match(op('values')), comma_sep(paren))

nestedexp = seq(
    op('('), choice(
        match(selexp, lambda s, v: [s]),
        match(valuesexp, lambda s, v: [s]),
        lambda s: nestedexp(s)),
    op(')'))

sqlexp = seq(choice(selexp, updexp, insexp, delexp, valuesexp), option(op(';')))

if __name__ == '__main__':
    print(selexp('select a from b t,c where (a = b)'))
    print(selexp('select a from b t,c'))
    print(selexp('SELECT ACCOUNTID, BALANCE, CREATIONDATE, LASTLOGIN, LOGINCOUNT, LOGOUTCOUNT, OPENBALANCE, PROFILE_USERID FROM accountejb WHERE (PROFILE_USERID = ?)'.lower()))
    print(updexp('UPDATE accountejb SET LOGOUTCOUNT = ? WHERE (ACCOUNTID = ?)'.lower()))
    print(selexp('SELECT t1.HOLDINGID, t1.PURCHASEDATE, t1.PURCHASEPRICE, t1.QUANTITY, t1.ACCOUNT_ACCOUNTID, t1.QUOTE_SYMBOL FROM accountejb t0, holdingejb t1 WHERE ((t0.PROFILE_USERID = ?) AND (t0.ACCOUNTID = t1.ACCOUNT_ACCOUNTID))'.lower()))
    print(sqlexp('INSERT INTO holdingejb (HOLDINGID, PURCHASEDATE, PURCHASEPRICE, QUANTITY, ACCOUNT_ACCOUNTID, QUOTE_SYMBOL) VALUES (?, ?, ?, ?, ?, ?)'.lower()))
    print(sqlexp('DELETE FROM orderejb WHERE (ORDERID = ?)'.lower()))
    print(sqlexp('select dept, LISTAGG(name, \',\') WITHIN GROUP (order by saraly desc nulls last, a asc) csv_name from listagg_sample group by dept'.lower()))
    print(sqlexp('select a as x from b t, (select c from d) u'))
    print(sqlexp('select a as x from b t left outer join ( select * from d ) u on t.i = u.i, e w'))
    print(sqlexp('select count(*) from t'))
    print(sqlexp('with t0 as ( select * from u ), t1 as ( select * from w ) select * from t0, t1'))
    print(sqlexp('select * from t inner join v on t.id = v.id'))
    print(sqlexp('select * from t union select * from u'))
    print(sqlexp("select case when true then 'abc' else col end from t"))
    print(sqlexp('select * from t group by x, y'))
    print(sqlexp('select a.*, count(*) over (partition by id) as c from a, b'))
    print(sqlexp('DELETE orderejb WHERE ORDERID = ?'.lower()))
    print(sqlexp("select * from ((select * from t) union (select * from d) order by x)"))
    print(sqlexp('select * from t for update'))
    print(condexp("a like '%' || ? ||'%'"))
    print(sqlexp('select t0.x, t1.y, t2.z, t3.w from a t0, (select * from b t1, c t2) as t3'))
    print(sqlexp('select d, trim(t.b) || trim(t.c) as a from t'))
    print(sqlexp('select t.a, s.a from s, (select * from x union select * from y) as t'))
    print(selexp('select a into b from c'))
    print(selexp('select set (a) into b from c'))
    print(sqlexp('update accountejb set lastLogin=?, logincount=logincount+1 where profile_userid=?'))
    print(sqlexp('update accountejb set balance = balance + ? where accountid = ?'))
    print(ascxt(match(qname))('a as b'))
    print(ascxt(colexp)('a'))
    print(ascxt(colexp)('a b'))
    print(colexp1('a'))
    print(colexp1('a b'))
    
