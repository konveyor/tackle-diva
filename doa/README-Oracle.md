# DOA for Oracle (since v2.1.0)

In version 2.1.0, assessment of SQL files that helps conversion from **PL/SQL (used by Oracle DBMS)** to PostgreSQL is introduced.
In future version, semi-automatic conversion from PL/SQL to Postgres will also be introduced.

This document is specific for Oracle support. For general document, see [README.md](README.md).

## Example

Let us try the PL/SQL file assessment using local files that we provide.

Being different from pulling application source from GitHub repo,
we need to specify `-f` option to make DiVA-DOA treat the argument as a directory name.
We also have to specify the dialect of the files using `-l` option, for which we specify `oracle`.

First go to `doa` directory by:

```bash
$ git clone .../tackle-diva.git
$ cd tackle-diva/doa
```

Then run the example is as follows:

```
bash ./run-doa.sh -i start_up.sh -l oracle -f "$(pwd)/plsql-example"
```

Output is as follows:

```
--------------------
DiVA-DOA wrapper
--------------------

running container diva-doa:latest...

------------------------
DiVA-DOA v2.1.0
------------------------
...

analyzing SQL scripts...
...

Analysis results:

Total number of SQLs : 2

Number of SQLs (Oracle dialects) : 1 (50.0%)
Number of SQLs (Generic): 1 (50.0%)

Number of SQLs automatically translated for Postgres: 1 (100.0%)
Number of SQLs requires manual revisions: 0 (0.0%)
  Local Index: 0
  Bitmap Index: 0

...
[OK] successfully completed.
```

Here assessment statistics is shown, which includes total number of files, ones with/without Oracle dialects, and possibility of automatic conversion that preserves its semantics.

**When successfully executed, manifest files are generated at `./output/app`.
Note that application name will be "app" when `-f` is specified.
Statistics of assessment results are also generated at `./output/app/stat/stats.json`.**

----

After the files are generated, continue from step (2) in [README](README.md).
Also note that only tables are created in this example.

Here briefly introduces commands and results in the example:

```
cd ./output/app
```

```
bash create.sh
```

Output:

```
configmap/app-cm-init-db created
configmap/app-cm-sqls created
job.batch/app-init created
postgresql.acid.zalan.do/app-db created
```

```
kubectl get all
```

```
kubectl apply -f test/pod-test.yaml
```

```
kubectl exec app-test -it -- bash
```

In the pod,

```
psql -h ${DB_HOST} -U postgres
```

psql session started:

```
psql (13.4 (Debian 13.4-4.pgdg110+1), server 13.6 (Ubuntu 13.6-1.pgdg18.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=# 
```

Show databases:

```
\dt
```

Output:

```
            List of relations
 Schema |     Name     | Type  |  Owner   
--------+--------------+-------+----------
 public | postgres_log | table | postgres
 public | table1       | table | postgres
 public | table2       | table | postgres
(3 rows)
```

Exit psql

```
\q
```

Exit from pod

```
exit
```

Delete test pod:

```
kubectl delete -f test/pod-test.yaml
```

Delete the cluster:

```
bash delete.sh 
```
