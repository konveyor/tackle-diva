# Tackle-DiVA-DOA
Tackle-DiVA Database Operator Adaption (DOA) toolchain. 

# Prerequisites

To try Quickstart, make sure that 

- A `minikube` or any other K8s cluster is started.
- Helm is installed.
- Postgres Operator (https://github.com/zalando/postgres-operator) is installed using Helm on `default` namespace of the cluster.

When you use `minikube`, check if it is working as follows:

<details>
<summary>How to check if you're using `minikube`</summary>

```bash
$ minikube status # check minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

$ kubectl cluster-info # check kubectl status
Kubernetes control plane is running at https://127.0.0.1:64533
CoreDNS is running at https://127.0.0.1:64533/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ helm version # check helm status
version.BuildInfo{Version:"v3.7.2", GitCommit:"663a896f4a815053445eec4153677ddc24a0a361", GitTreeState:"clean", GoVersion:"go1.17.3"}

$ helm list --filter 'postgres-operator' # check Postgres Operator
NAME                	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART                     	APP VERSION
postgres-operator   	default  	1       	2022-01-18 16:31:31.614054 +0900 JST	deployed	postgres-operator-1.7.1   	1.7.1      
postgres-operator-ui	default  	1       	2022-01-18 16:31:33.573745 +0900 JST	deployed	postgres-operator-ui-1.7.1	1.7.1      
```

`bash util/show-status.sh` to dump status shown above.

You can also check if UI of the operator is working using `minikube service`:

```bash
$ minikube service postgres-operator-ui
(messages shown) # a browser window for operator UI opens
(type Ctrl-C to terminate)
```

Note that `minikube service postgres-operator-ui` automatically opens a window for UI on your default browser, while `minikube service postgres-operator-ui --url` does not, just showing the expoed URL.
</details>


See [util/start-minikube.sh](util/start-minikube.sh) to (stop and) start a new minikube cluster and install operators using `bash` on macOS.

# Quickstart

Let us demonstrate the toolchain to adapt a `trading-app` app by saud-aslam (https://github.com/saud-aslam/trading-app).

## (0) Build `diva-migrator` docker image

Need to run just once.

```bash
$ make build

$ docker images diva-doa
REPOSITORY   TAG          IMAGE ID       CREATED        SIZE
diva-doa     2.0.0.dev0   0ef5158f0c85   44 hours ago   1.21GB
diva-doa     latest       0ef5158f0c85   44 hours ago   1.21GB
```

## (1) Analyze target app and generate manifests

To analyze `trading-app`, executing the wrapper script `run-doa.sh` with arguments:

```bash
$ bash ./run-doa.sh -o _out -i start_up.sh https://github.com/saud-aslam/trading-app
--------------------
DOA migrator wrapper
--------------------

running container...

------------------
DiVA migrator v1.0
------------------

...

[OK] successfully completed.
```

This code analyzes an app at repository https://github.com/saud-aslam/trading-app and outputs generated files under `_out` directory. You can specify any directory that you like.

In current version, you need to specify (by `-i` option) a file under the repository from which DB initializatoin code will be extracted. Currently only shell script file can be supported.

## (2) Create resources on a K8a cluster

Then let us create resources using the generated manifests. Since utility script is also generated, you can use it:

```bash
$ bash _out/create.sh
configmap/trading-app-cm-init-db created
configmap/trading-app-cm-sqls created
job.batch/trading-app-init created
postgresql.acid.zalan.do/diva-trading-app-db created
```

Then you can check resources' status by `kubectl get`:

```bash
$ kubectl get all 

# or 

$ kubectl get postgresql,svc,job,po,cm,secret,pvc,pv  # more detailed
```

For example, there should be 4 PostgreSQL instance Pods, one of which is a master and others are replica:

```
$ kubectl get po -l cluster-name=diva-trading-app-db -L spilo-role
NAME                    READY   STATUS    RESTARTS   AGE   SPILO-ROLE
diva-trading-app-db-0   1/1     Running   0          21m   master
diva-trading-app-db-1   1/1     Running   0          21m   replica
diva-trading-app-db-2   1/1     Running   0          21m   replica
diva-trading-app-db-3   1/1     Running   0          21m   replica
```

---

Before proceeding, you need to wait until the initialization Job and Pod finishes before proceeding:

```bash
# wait until STATUS of trading-app-init Pod becomes "Completed"
$ kubectl get pod -l job-name=trading-app-init
NAME                        READY   STATUS      RESTARTS   AGE
trading-app-init--1-z4zhc   0/1     Completed   4          8m18s
```

## (3) Check if the databses has been successfully created

### (3.1) Check via Postgres Operator UI

First you can confirm if the databases are created via operator UI:

```bash
$ minikube service postgres-operator-ui
(some messages shown) # a browser window for operator UI opens
```

It shows a UI of Postgres Operator in your browser. Clicking `PostgerSQL clusters` at top navigation shows the cluster that you have created. You can see its status and logs using the UI.
**In particular, you can see a message "cluster has been created" on the first line of log of the cluster.**

After you check, close the window and type `Ctrl-C` in your console to terminate `minikube service`.

### (3.2) Check via `psql` command

Next, let us check databases and tables using CLI.
You can use a Pod definition for test, which comes with generated manifests:

```bash
$ kubectl apply -f _out/test/trading-app-pod-init.yaml # creates a Deployment resource and associated Pod
deployment.apps/trading-app-init created
$ kubectl exec deploy/trading-app-init -it -- bash # login to the pod
```

In the pod, environment variables `DB_HOST` and `PGPASSWORD` are already set.

```bash
# connect to DBMS by specifying target database
$ printenv DB_HOST
diva-trading-app-db
$ printenv PGPASSWRD
(password shown)
```

So you can connect to databases and check if databases, tables, and views are successfully created.
Connect to cluster and database `jrvstrading` by 

```bash
$ psql -h ${DB_HOST} -U postgres -d jrvstrading 
```

or 

```bash
# connect to DBMS without specifying database
$ psql -h ${DB_HOST} -U postgres
\c jrvstrading # connect to database
```

and browse stuff:

```
jrvstrading=# \dt  # show tables
             List of relations
 Schema |      Name      | Type  |  Owner   
--------+----------------+-------+----------
 public | account        | table | postgres
 public | quote          | table | postgres
 public | security_order | table | postgres
 public | trader         | table | postgres
(4 rows)

jrvstrading-# \dv  # show views
                List of relations
 Schema |         Name          | Type |  Owner   
--------+-----------------------+------+----------
 public | pg_stat_kcache        | view | postgres
 public | pg_stat_kcache_detail | view | postgres
 public | pg_stat_statements    | view | postgres
 public | position              | view | postgres
(4 rows)

jrvstrading-# \q  # quit psql
$ exit         # (or Ctrl-D) to logout from the Pod
```

When checking is done, delete the test Pod:

```bash
$ kubectl delete -f _out/test/trading-app-pod-init.yaml
deployment.apps "trading-app-init" deleted
```

## (4) Delete resources created by step (2)

Executing `_out/delete.sh` deletes all resources created by `_out/create.sh`.

```bash
$ bash _out/delete.sh 
configmap "trading-app-cm-init-db" deleted
configmap "trading-app-cm-sqls" deleted
job.batch "trading-app-init" deleted
postgresql.acid.zalan.do "diva-trading-app-db" deleted
```

<details>
<summary>Resourcs after the cluster is deleted</summary>

```bash
$ kubectl get all
NAME                                        READY   STATUS    RESTARTS   AGE
pod/postgres-operator-594c75b5fc-hkwn9      1/1     Running   0          20m
pod/postgres-operator-ui-58644cfcff-tv77h   1/1     Running   0          20m

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kubernetes             ClusterIP   10.96.0.1       <none>        443/TCP    20m
service/postgres-operator      ClusterIP   10.100.238.88   <none>        8080/TCP   20m
service/postgres-operator-ui   ClusterIP   10.106.111.62   <none>        80/TCP     20m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/postgres-operator      1/1     1            1           20m
deployment.apps/postgres-operator-ui   1/1     1            1           20m

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/postgres-operator-594c75b5fc      1         1         1       20m
replicaset.apps/postgres-operator-ui-58644cfcff   1         1         1       20m

NAME                                                    IMAGE                                               CLUSTER-LABEL   SERVICE-ACCOUNT   MIN-INSTANCES   AGE
operatorconfiguration.acid.zalan.do/postgres-operator   registry.opensource.zalan.do/acid/spilo-14:2.1-p3   cluster-name    postgres-pod      -1              20m
```
</details>

That's all for the demonstration.

# For developers

See [docs/design.md](docs/design.md) for design document and development policy.
