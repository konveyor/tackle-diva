# DOA Toolchain Usage

Some usecases are considered:

## A. The toolchain **converts**, then **verifies** syntactically and semantiaclly

**In:** You need to turn on the `--convert` flag and specify source SQL directory `--in-dir` (or `-i`).

**Out:** Converted SQLs and several stat files including verification results are generated under the directory specified by `--out-dir` (or `-o`).

```bash
python -m sqal.cli --convert -i <source-dir> -o <output-dir>
```

## B. The toolchain only **verifies** syntactically and semantiaclly (with schema analysis results given)

**In:** You can start the toolchain with already converted files. Just need to run the toolchain by specifying (Postgres) SQL directory `--in-dir` (or `-i`) and the file of schema analysis result (before conversion) by `--schema-file` (or `-f`). 

If `-f` is omit, it tries to find under the `-i` directory with the default YAML name (`schema-info.yaml`). If it cannot be found, the tool behavior reduces to the case below.

**Out:** Both syntactic and semantic verification are performed and their results are generated under the directory specified by `--out-dir` (or `-o`).

```bash
python -m sqal.cli -i <converted-dir> -o <output-dir> -f <schema analysis file>
```


## C. The toolchain only **verifies** syntactically (without schema analysis results)

**In:** You can simply check syntax integrity of your SQL files. If you do not have schema analysis results before conversion, DOA only performs syntactic verification. Run the toolchain by specifying (Postgres) SQL directory `--in-dir` (or `-i`).

**Out:** Syntax verification results are generated under the directory specified by `--out-dir` (or `-o`).

```bash
python -m sqal.cli -i <converted-dir> -o <output-dir>
```
