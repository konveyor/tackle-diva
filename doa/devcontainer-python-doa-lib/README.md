# Dev container for DiVA-DOA container

Recommend to use this env on VS Code to develop `diva-doa` container content.
It installs `doa-lib` library just as external one and run testcases.

# How to connect

- `cd` to this folder.
- `code .` to start VS Code.
- Select `Reopen in Container` from command palette. See "Environment" for your development env.

# Environment

- Whole content of `tacke-diva/doa` is mounted on `/workspaces/doa`.
- Default workspace (= which code tree is shown at & new terminal windows open at) is located at `/workspaces/doa`.

# Files in `devcontainer-container`

Files/scripts for development of semantic verification.

- [.devcontainer](.devcontainer): Dev Container settings.
- [Makefile](Makefile): wrapper to test scripts.
- [0.in-oracle](0.in-oracle): Northwind DDL (for Oracle): a part from http://binaryworld.net/blogs/northwind-database-creation-script-for-sql-server/.
- [a.results](a.results): Output directory by the tool.

# How to test

To run the whole pipeline, `make case-a` and check if the output by DOA is saved in [a.resuls](a.results).

If you want to test each pipeline component, invoke each target in the Makefile such as 'split' or 'convert'.

# Memo (in Japanese)

## Conversion

物理的なサイズ以外に最大長制限のない BLOB 系データ型

Oracle: LONG (ラージ文字列), LONG RAW (ラージバイト列)
Postgres: TEXT (ラージ文字列), BYTEA (ラージバイト列)

## Semantic verification

informatino_schema を使ったテーブルスキーマの取得について、とくに FK 関係の取得:

- table_constraint を用いてテーブルに含まれる外部キー制約名を引く
- referential_constraint を用いて外部キー制約名に対応する一意 (または PK) 制約名を引く
- 上記制約名のそれぞれを key_column_usage で引くと各制約内の列名とそのインデックスが引けるので対応を取る

でいけるはず。


参考文献: https://stackoverflow.com/questions/3907879/sql-server-howto-get-foreign-key-reference-from-information-schema

### コードサンプル:

(1)

```bash
psql -c "\x" -c "select * from information_schema.table_constraints where table_name='territories' and constraint_type='FOREIGN KEY'"
```

```sql
select * from information_schema.table_constraints where table_name='territories' and constraint_type='FOREIGN KEY'
```

```text
Expanded display is on.
-[ RECORD 1 ]------+----------------------
constraint_catalog | postgres
constraint_schema  | public
constraint_name    | fk_territories_region
table_catalog      | postgres
table_schema       | public
table_name         | territories
constraint_type    | FOREIGN KEY
is_deferrable      | NO
initially_deferred | NO
enforced           | YES
```

(2)

```bash
psql -c "\x" -c "select * from information_schema.referential_constraints where constraint_name='fk_territories_region'"
```

```sql
select * from information_schema.referential_constraints where constraint_name='fk_territories_region'
```

```text
Expanded display is on.
-[ RECORD 1 ]-------------+----------------------
constraint_catalog        | postgres
constraint_schema         | public
constraint_name           | fk_territories_region
unique_constraint_catalog | postgres
unique_constraint_schema  | public
unique_constraint_name    | pk_region
match_option              | NONE
update_rule               | NO ACTION
delete_rule               | NO ACTION
```

`FK: fk_territories_region -> pk_region :PK` という対応関係

(3a) FK side

```bash
$ psql -c "\x" -c "select * from information_schema.key_column_usage where constraint_name='fk_territories_region'"
```

```sql
select * from information_schema.key_column_usage where constraint_name='fk_territories_region'
```

```text
Expanded display is on.
-[ RECORD 1 ]-----------------+----------------------
constraint_catalog            | postgres
constraint_schema             | public
constraint_name               | fk_territories_region
table_catalog                 | postgres
table_schema                  | public
table_name                    | territories
column_name                   | regionid
ordinal_position              | 1
position_in_unique_constraint | 1
```

(3b) PK side

```bash
$ psql -c "\x" -c "select * from information_schema.key_column_usage where constraint_name='pk_region'"
```

```sql
select * from information_schema.key_column_usage where constraint_name='pk_region'
```

```text
Expanded display is on.
-[ RECORD 1 ]-----------------+----------
constraint_catalog            | postgres
constraint_schema             | public
constraint_name               | pk_region
table_catalog                 | postgres
table_schema                  | public
table_name                    | region
column_name                   | regionid
ordinal_position              | 1
position_in_unique_constraint | 
```

(3a) (3b) により、`territories.regionid (ordinal=1)` が `region.regionid (position=1)` に対応していることがわかる。この ordinal を使えば、複数列の FK-PK 関係も捉えられるはず。


(まとめる)

FK 側

```sql
select * from information_schema.table_constraints as tc, information_schema.referential_constraints as rc, information_schema.key_column_usage as cu1, information_schema.key_column_usage as cu2 where tc.table_name='territories' and tc.constraint_type='FOREIGN KEY' and rc.constraint_name=tc.constraint_name and cu1.constraint_name=rc.constraint_name and cu2.constraint_name=rc.unique_constraint_name and cu1.position_in_unique_constraint=cu2.ordinal_position;
```

以下、`%s` 部分に調査したいテーブル名を入れる

```sql
select tc.constraint_catalog, tc.constraint_schema, tc.table_name, cu1.column_name as column_name_1, cu2.column_name as column_name_2 from information_schema.table_constraints as tc, information_schema.referential_constraints as rc, information_schema.key_column_usage as cu1, information_schema.key_column_usage as cu2 where tc.table_name=%s and tc.constraint_type='FOREIGN KEY' and rc.constraint_name=tc.constraint_name and cu1.constraint_name=rc.constraint_name and cu2.constraint_name=rc.unique_constraint_name and cu1.position_in_unique_constraint=cu2.ordinal_position group by tc.constarint_name;
```

(例) territories の例

```text
psql -c "\x" -c "select tc.constraint_catalog, tc.constraint_schema, tc.table_name, array_agg(cu1.column_name) as column_name_1, array_agg(cu2.column_name) as column_name_2 from information_schema.table_constraints as tc, information_schema.referential_constraints as rc, information_schema.key_column_usage as cu1, information_schema.key_column_usage as cu2 where tc.table_name='territories' and tc.constraint_type='FOREIGN KEY' and rc.constraint_name=tc.constraint_name and cu1.constraint_name=rc.constraint_name and cu2.constraint_name=rc.unique_constraint_name and cu1.position_in_unique_constraint=cu2.ordinal_position group by tc.constraint_catalog, tc.constraint_schema, tc.table_name, tc.constraint_name;"
```

```text
Expanded display is on.
-[ RECORD 1 ]------+------------
constraint_catalog | postgres
constraint_schema  | public
table_name         | territories
column_name_1      | {regionid}
column_name_2      | {regionid}
```
