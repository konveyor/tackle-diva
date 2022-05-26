# Conversion Analysis Details

When `-l` option is given, *DOA* treats SQL files as in the specified dialect.
It parses and analyzes each of the files to check if it can be **equivalently** converted for PostgreSQL.
- If possible, the file will be converted and stored into `cm-sqls.yaml`, a ConfigMap definition.
- Otherwise it requires human revision and will not be converted. The file will not be stored into the ConfigMap.

At the point of writing, `oracle` is only accepted value of the `-l` option.

> See [README-Oracle.md](../README-Oracle.md) for tool usage.

Result of analysis is shown on console as follows:

```
Analysis results:

Total number of SQLs: 1154

Number of SQLs (Oracle dialects): 1154 (100.0%)
Number of SQLs (Generic): 0 (0.0%)

Number of SQLs automatically translated for Postgres: 1150 (99.7%)
Number of SQLs required manual revisions: 4 (0.3%)
  Local Index: 4
  Bitmap Index: 0
```

Also detailed statistics is saved as a JSON file:

```json
[ "json file comes here..." ]
```

## Dialect Syntaxes 

**PL/SQL**, that is a SQL dialect that Oracle are using, has a number of their unique syntaxes.
We briefly describe them in the next subsections.

| ID | Description| Convertible? | - | Remarks/Conversion |
|--|--|--|--|--|
|1| REMARK (REM) statement | ✓ | - | Remove. |
|2| `/`-only line (executing buffer) | ✓ | - | Replace with `;`. |
|3| Non-rsvd keyword `LIMIT` | ✓ | - | Quote the name. |
|4| Oracle-specific types | ✓ | - | Convert to standard or PostgreSQL types. |
|5| `ALTER TABLE ... MODIFY` | ✓ | - | Rewrite parse tree. |
|6| `ALTER TABLE ... ADD` | ✓ | - | Rewrite parse tree. | 
|7| `ALTER TABLE ... ADD CONSTRAINT` | | - | Rewrite parse tree. |
|8| `BITMAP` | ❎ | - | BITMAP index | 
|9| `LOCAL` | ❎ | - | LOCAL index | 
|10| Physical properties (tablespaces) `STORAGE`/`LOB` | ❎ | - | physical property なので前処理で削除 |

## Non-Dialect

| ID | Description| Convertible? | - | Remarks/Conversion |
|--|--|--|--|--|
|100| Non-existent schema |  | - | `ERROR:  schema "tqnet" does not exist` に起因。暫定的にスキーマを手動で作る。 | 

---

##  A. Convertible Syntaxes

### [1] REMARK (REM) statement

Single-line comments used in Oracle.

### [2] `/`-only line (executing buffer)

When only `/` appears in a line, it means "execute buffer content". This is equivalent to `;` in the almost cases.

### [3] Non-reserved keyword

`LIMIT` is used as a column name, which is a non-reserved keyword in Oracle, while reserved one in Postgres. We avoid errors by enlosing it by quotes: `LIMIT` -> `"LIMIT"`.

### [4] Oracle-specific types

- Convert `NUMBER` to `DECIMAL`.
- Convert `VARCHAR2` to `VARCHAR`.
- Convert `BLOB` to `BYTEA`.

### [5] `ALTER TABLE ... MODIFY`

Convert 

```sql
ALTER TABLE <table> MODIFY (<col> <type>, ...)
```
to 

```sql
ALTER TABLE <table>
    ALTER COLUMN <col> TYPE <type>,
    ...
;
```

### [6] `ALTER TABLE ... ADD`

Convert 

```sql
ALTER TABLE <table> ADD (<columns>)...
```

to 

```sql
ALTER TABLE <table>
    ADD COLUMN <col> TYPE <type>,
    ...
;
```

### [7] `ALTER TABLE ... ADD CONSTRAINT`

Convert 

```sql
ALTER TABLE <table>
    ADD (CONSTRAINT <name> ...)
```

to 

```sql
ALTER TABLE <table>
    ADD CONSTRAINT <name> ...
```

## B. Non-convertible Syntaxes

### [8] `BITMAP`

### [9] `LOCAL`

### [10] Physical properties (tablespaces) `STORAGE`/`LOB`

---

## C. Backlog

- `PARTITION BY` (Postgres also have `PARTITON BY` but syntax and semantics are bit different.)
- `LONG RAW`: variable length binary data (differernt from `BLOB`?)
- `CHAR (1 BYTE)`
- `SUBSTRB(...)`
    - seems to be **functional-based indexes** (see also https://docs.oracle.com/cd/E16338_01/server.112/b56299/functions181.htm)

      ```sql
      CREATE INDEX KTQ800118FNC
          ON CTQ8001 ( SUBSTRB( R_VIN,1,3 ) );
      ```
