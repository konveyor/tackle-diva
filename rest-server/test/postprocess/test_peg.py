from diva_server.postprocess.peg import before, match, seq, star, val

peg0 = seq(val('{'),
           star(seq(before('{', '}'), lambda s: peg0(s))),
           before('{', '}'),
           val('}'))
peg1 = star(seq(before('{', '}'), match(peg0)))


def test_1():
    x0, x1 = star(val('a'))('aaa')
    assert x0 == ''
    assert x1 == []


def test_2():
    x0, x1 = peg0('{aaa}')
    assert x0 == ''
    assert x1 == []


def test_3():
    x0, x1 = peg1(
        'akihiko.plugins.HttpRequestAnalyzer@3af87954={method=[POST, GET], path=/app, action=[login, {home}], passwd=xxx}, b={}')
    assert x0 == ''
    assert len(x1) == 2
    assert x1[0] == '{method=[POST, GET], path=/app, action=[login, {home}], passwd=xxx}'
    assert x1[1] == '{}'
