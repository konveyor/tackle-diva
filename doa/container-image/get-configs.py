"""
Get configrations from pyproject.toml in python-doa-lib.

The global configuration of the DOA toolchain is stored there.
You need to install TOML Kit (tomlkit) to run this script.

"""
from typing import Optional

from tomlkit import load
from typer import Abort, Typer, echo

app=Typer()

def load_toml(file:Optional[str])->dict:
    "load a toml file and returns loaded dict."
    with open(file, mode="r", encoding="utf-8") as f:
        return load(f)

def doa_config(data:dict, key:Optional[str]=None)->dict:
    "returns data for the [tool.doa] section."
    if key:
        return data["tool"]["doa"][key]
    return data["tool"]["doa"]

def poetry_config(data:dict,key:str=None)->dict:
    "returns data for the [tool.poetry] section."
    if key:
        return data["tool"]["poetry"][key]
    return data["tool"]["poetry"]

@app.command()
def main(kind:str):
    data = load_toml("../python-doa-lib/pyproject.toml")
    if kind=="image-name":
        print(doa_config(data, "image-name"))
    elif kind=="version":
        print(poetry_config(data,"version"))
    else:
        echo(f"unknown kind: {kind}")
        Abort()
        
if __name__ == "__main__":
    app()
