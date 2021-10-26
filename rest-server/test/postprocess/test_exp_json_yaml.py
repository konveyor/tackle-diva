"""experiments on key order between json and pyyaml modules."""
import json
from pprint import pprint

import yaml


def _sub(s, **kwargs) -> None:
    d = json.loads(s, **kwargs)
    pprint(d)
    for x in d.items():
        print(x)
    print('='*10)
    y1 = yaml.dump(d, default_flow_style=False)
    print(y1)
    print('='*10)
    y2 = yaml.dump(d, default_flow_style=False, sort_keys=False)
    print(y2)
    print('='*10)
    y3 = yaml.dump(d, default_flow_style=True, sort_keys=False)
    print(y3)


def f(pairs):
    print(pairs)
    a = dict()
    a.update(pairs)
    return a


def test1() -> None:
    print('deault:')
    _sub('{"z":1, "y":2, "x":3}')


def test2() -> None:
    print('dict:')
    _sub('{"z":1, "y":2, "x":3}', object_pairs_hook=dict)


def test3() -> None:
    d = json.loads('{"z":1, "y":2, "x":3}', object_pairs_hook=f)
    pprint(d)
    for x in d.items():
        print(x)
