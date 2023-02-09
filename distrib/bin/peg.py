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

def pegop(f):
    def g(*args):
        memo = [None] * 64
        def h(s):
            i = hash(s) % 64
            if memo[i] and memo[i][0] == s:
                return memo[i][1]
            else:
                v = f(s, *args)
                memo[i] = (s, v)
                return v
        return h
    return g

def pegcxt(f):
    def g(e):
        c = []
        c.append(f(e, lambda s:c[0](s)))
        return c[0]
    return g

@pegop
def choice(s, *args):
    for f in args:
        a = f(s)
        if a is not ():
            return a
    return ()

@pegop
def seq(s, *args):
    r = []
    for f in args:
        a = f(s)
        if a is ():
            return ()
        s = a[0]
        r += a[1]
    return s, r

@pegop
def val(s, x):
    if s.startswith(x):
        return s[len(x):], []
    else:
        return ()

@pegop
def before(s, *args):
    t = None
    for a in args:
        if a is None:
            t = '' if t is None else t
        elif a in s and (t is None or (len(s) - s.index(a)) > len(t)):
            t = s[s.index(a):]
    if t is None:
        return ()
    else:
        return t, []

@pegop
def match(s, e, r=None):
    a = e(s)
    if a is ():
        return ()
    elif r is None:
        return a[0], a[1] + [s[:len(s)-len(a[0])]]
    else:
        return a[0], r(a[1], s[:len(s)-len(a[0])])

@pegop
def debug(s, e):
    print("debug:", s)
    return e(s)

@pegop
def star(s, e):
    r = []
    while 1:
        a = e(s)
        if a is ():
            return s, r
        s = a[0]
        r += a[1]

def nil(s):
    return s, []


if __name__ == '__main__':
    peg0 = seq(val('{'),
               star(seq(before('{', '}'), lambda s : peg0(s))),
               before('{', '}'),
               val('}'))
    peg1 = star(seq(before('{', '}'), match(peg0)))
    print(star(val('a'))('aaa'))
    print(peg0('{aaa}'))
    print(peg1('akihiko.plugins.HttpRequestAnalyzer@3af87954={method=[POST, GET], path=/app, action=[login, {home}], passwd=xxx}, b={}'))
