# java-env

Java environment for parser generation, which is needed to generate a PL/SQL parser using ANTLR v4.
Recommended to develop grammar and genearates parser under Dev Container of VS Code.

## Files

- .devcontainer/
  - Dev Container settings.
- org/
  - Original grammar definitions (`*.g4`) and support classes (`*.py`) for PL/SQL. Kept for reference.
  - Copied from https://github.com/antlr/grammars-v4/tree/master/sql/plsql 
  - Note: licensed under the APL 2.0 (the Apache License, Version 2.0).
- in/
  - Grammar definitions (`*.g4`) and support classes (`*.py`) for PL/SQL, **being modified to support older PL/SQL.**
- plsql/
  - Generated files from the grammar.
- Makefile
  - Makefile to generate the parser.
- examples/
  - Sample grammar `Hello.g4` to test parser generation and parsing.

## How to generate parser

First, check if ANTLR is properly installed:

```
make test
```

Usage of the generator is shown.
Then, try this command to generate the parser:

```
make gen
```

Python codes are generated under `plsql/`.

## Cleanup


To delete all generated files,

```
make clean
```
