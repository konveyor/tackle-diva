"""test for sqlparse.py, copied from its main routine."""
from pprint import pprint

from diva_server.postprocess.sqlparse import condexp, selexp, sqlexp, updexp


def test_01():
    # 't' is a table alias where 'as' is omitted here.
    x = selexp('select a from b t,c where (a = b)')
    # pprint(x)
    assert x == (
        '',
        [
            'select',
            {'a': ('a',)},
            {':from': [{'t': 'b'}, 'c']},
            ('a',),
            ('b',)
        ]
    )


def test_02():
    x = selexp('select a from b t,c')
    # pprint(x)
    assert x == (
        '',
        [
            'select',
            {'a': ('a',)},
            {':from': [{'t': 'b'}, 'c']}
        ]
    )


def test_03():
    s = 'SELECT ACCOUNTID, BALANCE, CREATIONDATE, LASTLOGIN, LOGINCOUNT, LOGOUTCOUNT, OPENBALANCE, PROFILE_USERID FROM accountejb WHERE (PROFILE_USERID = ?)'.lower(
    )
    # print(s)
    x = selexp(s)
    # pprint(x)
    assert x == (
        '',
        [
            'select',
            {'accountid': ('accountid',)},
            {'balance': ('balance',)},
            {'creationdate': ('creationdate',)},
            {'lastlogin': ('lastlogin',)},
            {'logincount': ('logincount',)},
            {'logoutcount': ('logoutcount',)},
            {'openbalance': ('openbalance',)},
            {'profile_userid': ('profile_userid',)},
            {':from': ['accountejb']},
            ('profile_userid',)
        ]
    )


def test_04():
    s = 'UPDATE accountejb SET LOGOUTCOUNT = ? WHERE (ACCOUNTID = ?)'.lower()
    # print(s)
    x = updexp(s)
    # pprint(x)
    assert x == (
        '',
        [
            'update',
            {':from': ['accountejb', ('logoutcount',)]},
            ('accountid',)
        ]
    )


def test_05():
    s = 'SELECT t1.HOLDINGID, t1.PURCHASEDATE, t1.PURCHASEPRICE, t1.QUANTITY, t1.ACCOUNT_ACCOUNTID, t1.QUOTE_SYMBOL FROM accountejb t0, holdingejb t1 WHERE ((t0.PROFILE_USERID = ?) AND (t0.ACCOUNTID = t1.ACCOUNT_ACCOUNTID))'.lower(
    )
    # print(s)
    x = selexp(s)
    # pprint(x)
    assert x == (
        '',
        [
            'select',
            {'holdingid': ('t1.holdingid',)},
            {'purchasedate': ('t1.purchasedate',)},
            {'purchaseprice': ('t1.purchaseprice',)},
            {'quantity': ('t1.quantity',)},
            {'account_accountid': ('t1.account_accountid',)},
            {'quote_symbol': ('t1.quote_symbol',)},
            {':from': [{'t0': 'accountejb'}, {'t1': 'holdingejb'}]},
            ('t0.profile_userid',),
            ('t0.accountid',),
            ('t1.account_accountid',)
        ]
    )


def test_06():
    x = sqlexp('INSERT INTO holdingejb (HOLDINGID, PURCHASEDATE, PURCHASEPRICE, QUANTITY, ACCOUNT_ACCOUNTID, QUOTE_SYMBOL) VALUES (?, ?, ?, ?, ?, ?)'.lower())
    # pprint(x)
    assert x == (
        '',
        [
            'insert',
            {':from': ['holdingejb',
                       ('holdingid',),
                       ('purchasedate',),
                       ('purchaseprice',),
                       ('quantity',),
                       ('account_accountid',),
                       ('quote_symbol',)]}
        ]
    )


def test_07():
    "invalid syntax example."
    x = sqlexp('DELETE FROM orderejb WHERE (ORDERID = ?'.lower())
    # pprint(x)
    assert x == (
        ' where (orderid = ?',
        ['delete', {':from': ['orderejb']}]
    )


def test_08():
    x = sqlexp('select dept, LISTAGG(name, \',\') WITHIN GROUP (order by saraly desc nulls last, a asc) csv_name from listagg_sample group by dept'.lower())
    pprint(x)


def test_09():
    x = sqlexp('select a as x from b t, (select c from d) u')
    pprint(x)


def test_10():
    x = sqlexp(
        'select a as x from b t left outer join ( select * from d ) u on t.i = u.i, e w')
    pprint(x)


def test_11():
    x = sqlexp('select count(*) from t')
    pprint(x)


def test_12():
    print(sqlexp('with t0 as ( select * from u ), t1 as ( select * from w ) select * from t0, t1'))


def test_13():
    print(sqlexp('select * from t inner join v on t.id = v.id'))


def test_14():
    print(sqlexp('select * from t union select * from u'))


def test_15():
    print(sqlexp("select case when true then 'abc' else col end from t"))


def test_16():
    print(sqlexp('select * from t group by x, y'))


def test_17():
    print(sqlexp('select a.*, count(*) over (partition by id) as c from a, b'))


def test_18():
    print(sqlexp('DELETE orderejb WHERE (ORDERID = ?'.lower()))


def test_19():
    print(sqlexp("select * from ((select * from t) union (select * from d) order by x)"))


def test_20():
    print(sqlexp('select * from t for update'))


def test_21():
    print(condexp("a like '%' || ? ||'%'"))


def test_22():
    print(sqlexp('select t0.x, t1.y, t2.z, t3.w from a t0, (select * from b t1, c t2) as t3'))


def test_23():
    print(sqlexp('select d, trim(t.b) || trim(t.c) as a from t'))


def test_24():
    print(sqlexp('select t.a, s.a from s, (select * from x union select * from y) as t'))


def test_25():
    print(selexp('select a into b from c'))


def test_26():
    print(selexp('select set (a) into b from c'))
