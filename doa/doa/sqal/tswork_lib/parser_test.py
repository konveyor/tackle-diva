"""
parsing test using sqlparse library.
"""
from os import environ
from pathlib import Path

import sqlparse

if __name__ == "__main__":
    root = Path(environ["TQ_NET_ROOT"]) / \
        "../TQ-NET/02.定義/02_DB_UTF/tq01_cre_tab"
    infile = root / "cer01e800.sql"
    with open(infile, encoding="utf-8") as f:
        for l in sqlparse.parse(sql=f.read()):
            print("[LINE] " + str(l))
