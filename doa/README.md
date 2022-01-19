# Tackle-DiVA-DOA
Tackle-DiVA Database Operator Adaption (DOA) toolchain. 

**Demonstration using sample app is ready. See below for the demo.**

# Prerequisites

- Make sure that a `minikube` or any other K8s cluster is started.
- Helm is installed.
- Postgres Operator is installed (using Helm) on `default` namespace of the cluster.

When you use `minikube`, check if it is working as follows:

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

You can also check if UI of the operator is working using `minikube service`:

```bash
$ minikube service postgres-operator-ui
(messages shown) # a browser window for operator UI opens
(type Ctrl-C to terminate)
```

Note that `minikube service postgres-operator-ui` automatically opens a window for UI on your default browser, while `minikube service postgres-operator-ui --url` does not, just showing the expoed URL.

See [util/start-minikube.sh](util/start-minikube.sh) to start a minikube cluster and install operators using `bash` on macOS.

# Quickstart

Imagine that we demonstrate the tool to adapt a `trading-app` app by saud-aslam at https://github.com/saud-aslam/trading-app.

## (0) Build `diva-migrator` docker image

Need to run just once. (TODO: Makefile to be changed to a shell script)

```bash
make build
```

> If you want to build the image by yourself, make sure to specify a build-time variable `IMAGE_VER` to `docker build`. If not specified, `unknown` will be used.
> Built image have labels `project` (whose value is `diva`), `name` (`migrator`), and `version` (specified value by the build-arg above).

## (1) Analyze target app

To analyze `trading-app`, executing the wrapper script `run-doa.sh` with arguments:

<!--
```bash
docker run -it --rm -v $(readlink -f _out):/out diva-migrator:latest \
    -o /out https://github.com/saud-aslam/trading-app
```
-->

```bash
bash ./run-doa.sh -o _out -i start_up.sh https://github.com/saud-aslam/trading-app
```

This code analyzes an app at repository https://github.com/saud-aslam/trading-app and outputs generated files under `_out` directory. You can specify any directory that you like.

In current version, you need to specify (by `-i` option) a file under the repository from which DB initializatoin code will be extracted. Currently only shell script file can be supported.

## (2) Create resources on a K8a cluster

Then let us create resources using the generated manifests. Since utility script is also generated, you can use it:

```bash
bash _out/create.sh
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

Before proceeding, you need to wait until the initialization Job finishes before proceeding:

```bash
# wait until the completion status of the trading-app-init Job becomes 1/1...
$ kubectl get job -w
NAME               COMPLETIONS   DURATION   AGE
trading-app-init   1/1           17s        6m14s
# type Ctrl-C to exit
$
```

## (3) Check if the databses has been successfully created

First you can confirm if the databases are created via operator UI:

```bash
$ minikube service postgres-operator-ui
(some messages shown) # a browser window for operator UI opens
```

It shows a UI of Postgres Operator in your browser. Clicking `PostgerSQL clusters` at top navigation shows the cluster that you have created. You can see its status and logs using the UI.
After you check, close the window and type `Ctrl-C` in your console to terminate `minikube service`.

Next, let us check databases and tables using CLI.
You can use the Deployment definition for test which comes with generated manifests:

```bash
kubectl apply -f _out/test/trading-app-pod-init.yaml # creates a Deployment resource and associated Pod
kubectl exec deploy/trading-app-init -it -- bash # login to the pod
```

In the pod, environment variables `DB_HOST` and `PGPASSWORD` are already set, thus you can connect to databases and check if databases, tables, and views are successfully created.

Connect to cluster and database `jrvstrading` by 

```bash
# connect to DBMS by specifying target database
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
\dt            # show tables
\dv            # show views
\q             # quit psql
exit           # (or Ctrl-D) to disconnect from DB
$ exit         # (or Ctrl-D) to logout from the Pod
```

When checking is done, delete the test Pod using the manifest used to create it:

```bash
kubectl delete -f _out/test/trading-app-pod-init.yaml
```

## (4) Delete resources created by step (2)

Executing `_out/delete.sh` deletes resources created by `_out/create.sh`.

```bash
bash _out/delete.sh
```

That's all for the demonstration.

----
# For developers

## Releases (Tags)

- `v1.0.0`: first release. (Nov., 2021)

## Branches

- `main`: the main branch (and dev branch for v2). See this branch for the latest revision.
  - You cannot directly push to `main` branch. Need to create a PR.
- `v1`: ver. 1 release branch.
