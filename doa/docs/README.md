# Work Memo

My experiments and findings to be appeared.

## Work #2

参考: https://github.ibm.com/trl-data-modern/diva-doa/issues/2

脆弱性
- GitHub が `pom.xml` の httpclient に対して脆弱性警告。
あとでバージョンアップしてみる。

### start-up.sh
動かない。
- jrvs-psql は立ち上がらない。
  - そもそも、docker コマンドにイメージ名が指定されていないなど
- psql をローカルで実行している
- Java をローカルで実行している
- jrvsーsql の /docker-entrypoint-initdb.d/ 中で指定する SQL ファイルが誤っている？
  - 一方でイメージ起動後にも同様のファイルを外から実行している
- なお、2つのコンテナ自体は作ってある

対策: それらを適切に書き換えた上で docker-compose ファイルを作る?
- psql/Dockerfile の修正


動くようになったらそれが自動化解析の starting point.

### 議論 

(w/ 勝野さん) 動かすこと自体が目的ではないので、スキップして #3 に進むこととする。

## Work #3

参考: https://github.ibm.com/trl-data-modern/diva-doa/issues/3

新しい minikube (と kubectl) を入れる (brew 経由。バージョン違いなどでトラブったらソースインストール)

```
brew update
brew upgrade minikube
brew upgrade kubernetes-cli
```

> 新規インストールについて:
> `brew install --cask docker` で Docker を入れると `kubectl` もインストールされる。
> 一方で、`brew install minikube` は `kubernetes-cli` に依存し、これによっても `kubectl` がインストールされる。
> これを解消するには `brew link --overwrite kubernetes-cli` を実行。これにより後者によるシンボリックリンクが有効になる。

### Versions

- macOS Big Sur 11.6
- Docker (via binary package):
  - Docker Desktop: 4.1.1
  - Docker Engine: 20.10.8
  - Kubernetes: v1.21.5
- minikube (via brew): v1.23.2 → v1.24.0
- kubectl (via brew): client: v1.22.2 → v1.22.3
- hyperkit (via Dockder?): v0.20210107-12-gadc4ea

ちょっとバージョンがあってないのが気になる。

### Start up a minikube cluster

Driver に Docker を使うと制限があるらしいので HyperKit を指定してみようと思ったが、うまく行かなかったので、デフォルトの Docker を使用した。その代わり Ingress が使えないらしいが、今回は問題ない。

```bash
# minikube config set driver docker
# minikube config view
minikube delete
minikube start [--driver=docker]
minikube dashboard
kubectl get po -A 
```

### Install the Postgres Operator

Helm 入れてみる:

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

入った。

```
$ helm version
version.BuildInfo{Version:"v3.7.1", GitCommit:"1d11fcb5d3f3bf00dbe6fe31b8412839a96b3dc4", GitTreeState:"clean", GoVersion:"go1.16.9"}
```

Posgres Operator を Helm で入れてみる:

```bash
git clone https://github.com/zalando/postgres-operator.git
cd postgres-operator/
git checkout refs/tags/v1.7.0 # not needed?
# helm show values ./charts/postgres-operator # show variable values
helm install postgres-operator ./charts/postgres-operator
helm install postgres-operator-ui ./charts/postgres-operator-ui
```

確認

```
helm list
kubectl --namespace=default get pods -l "app.kubernetes.io/name=postgres-operator"
kubectl --namespace=default get pods -l "app.kubernetes.io/name=postgres-operator-ui"
```

上手くいかないときには、Pod の情報を表示する。

```
kubectl describe po <pod ID>
```

<!-- ```
ibmcloud login -sso
ibmcloud ks cluster config --cluster diva-dao
kubectl config current-context
``` -->

起動したっぽいので UI を表示する

```
kubectl port-forward svc/postgres-operator-ui 8081:80
```

これは foreground コマンド。
(ただしくは route を設定するべき? → OSC に route はあるけど K8s にはなかった)

ブラウザで `localhost:8081` が表示された。default の ns のままで動いた。

### DB クラスタ作成

次は custom resource `postgresql` の作成。上記 UI でも作れるし、`kubectl create` でも作れる。
(実際には `kubectl apply` のほうがよいと思われる)

```bash
kubectl apply -f manifests/minimal-postgres-manifest.yaml # オリジナルのほうの manifest
```

IBM Cloud の K8s クラスタが無料で使えたので途中までやっていたが、PV が作れなくてエラーになることが判明。

> Pod のスタートに失敗。エラーメッセージは

> ```
> 0/1 nodes are available: 1 pod has unbound immediate PersistentVolumeClaims.
> ```

> Persistent Volume (以下 PV) を作成していないからだと判断。ダッシュボードから作成することにする。

結局、無料では作れなさそうだったので、mac の minikube でやることにした。(ドライバの問題は解決したので)

DB pod の表示:

```bash
kubectl get po -l application=spilo -L spilo-role
```

次にスケーリングのテスト。
この repo にある manifest file をつかってレプリカ数を変更してみる:

```bash
# cd diva-doa
kubectl kubectl apply -f manifests/minimal-postgres-manifest.yaml
```

クラスタの pod が増えてるはず。

`kubectl patch` でもいけるはず:

```bash
kubectl patch postgresql acid-minimal-cluster --type=merge -p '{"spec":{"numberOfInstances":6}}'
```

なお、これは JSON merge patch という。`--type=json` とすると、JSON patch という違う形式の patch を要求するので注意。JSON patch は

```json
[
  {
    "op": "...",
    "path": "...",
    "value": "..."
  }
]
```
みたいな形式の patch のこと。

### DB への接続 (Pod から)

実験用 pod 作る:

```
kubectl run test-client -it --image=postgres --command -- bash
```

~~そもそもは DBMS 用のコンテナなので、postgres ユーザのパスワードを指定する必要がある。~~

Pod の環境変数として secret の値を渡す方法はあるが、まずはコピペベースで試す。
Postgres のユーザごとのクレデンシャル secret が作られているので、

```
kubectl get secret
```

で一覧が表示できる。デフォルトの `postgres` と、マニフェストの `.spec.users` で指定したユーザ分の secret が作られる。

取り出しはこうする (secret には `password` と `username` が入っている):

```
kubectl get secret zalando.acid-minimal-cluster.credentials.postgresql.acid.zalan.do -o jsonpath="{.data.password}" | base64 -d
```

これを使って、
Pod 内で 

```
root@test-client:/# psql -h acid-minimal-cluster -U zalando foo
```

パスワードを聞かれるので、取得した secert をコピーしてきて入力する。
ログインできた。
- `\l` でデータベース一覧を表示できる
- テーブルは定義されていないので `\dt` で何も表示されない。

### DB への接続 (外部から)

`minikube tunnel` の記事を見てたけど、`minikube service <svc> --url` で動いているように見える。
ClusterIP モードのままで問題なく動いているように見える。minikube のドライバ指定が Docker の場合、警告が表示されるが、ブラウザではなくてターミナルから試す場合にはこれで問題ない。

実行すると割当ポートが指定されるので、例えば

```
psql -h localhost -p 54132 -U zalando foo
```

で同じように接続できる。

### HA (レプリケーション) のテスト

> (再掲) `spilo-role` の値で DB インスタンスが master か replica かわかる。

専用の Pod を作った。ログインアカウントが環境変数 `USER` と `PASS` に設定されている。

```bash
kubectl apply -f manifests/testpod.yaml
kubectl exec test-pg-55b485dff6-ddq8d -it -- bash # pod 名は目視からベルから判断
```

なお、`PGPASSWORD` にパスワードを設定しておくと楽だが非推奨。`.pgpass/` を使ったほうがよい。

```bash
PGPASSWORD=${PASS} psql -h <IP of a DB> -U ${USER} foo
\l # list DBs
\dt # list tables in the current DB
```

なんかテーブルを作ってみる

```sql
create table record (
  id integer,
  name varchar(10)
);
insert into record values ( 1, 'shin saito' );
select * from record;
```

ここでログアウトして、master を殺す。

```bash
kubectl delete pod <master DB pod>
```

新しいノードが立って master の再設定が行われる。
再びどれかの Pod に接続しなおして中身を見てみる。

```bash
# 略
\dt # record table があることを確認
select * from record;
```

## Work #4

参考: https://github.ibm.com/trl-data-modern/diva-doa/issues/4

目標: Trading-app を K8s アプリとして動かすこと、そのために必要な定義をまとめる。

用語:

- アプリ: ここではフロントエンド側の Java アプリのこと。Java。Spring Boot 使用。
- DB: ここでは Postgres DB のこと。

構成:
- イメージ定義 (= Dockerfile)
  - アプリ側はそのまま使用
  - DB側は、初期化スクリプト (の一部) が指定されていることを覚えておく
    - 2つあるうち、1つ (アクセス権設定) しか指定されていない。
- Pod 定義 (2つ)
  - アプリ用
  - DB 用
- DB の初期化スクリプト (2種類)
- DB の接続先設定

とりあえず diva-app/out/ 以下においてある:
- setup-kube.sh: minikube を設定してクラスタを作成、Operator などのインストールを行う
  - setup-op.sh: 上記のうち Operator のインストール部分。**あらかじめ Operator の repo を clone しておくことが必要。**
- run-trading-app.sh: 必要なイメージをビルドして minikube 上でアプリを実行。初回のみイメージのビルドに数分かかる。複数の YAML に分けてるけど、一つにするかもしれない。また、service の expose は kubectl でやっているが、マニフェストに入れてしまうほうがいいかもしれない。
  - frontend.yaml: フロントエンド用のマニフェスト (1 Deployment)
  - db.yaml: DB用のマニフェスト (未製作)

## Work #5

参考: https://github.ibm.com/trl-data-modern/diva-doa/issues/5

## Work #6

参考: https://github.ibm.com/trl-data-modern/diva-doa/issues/6

## Migration の自動化には何が必要か?

- データベースの初期化スクリプトはどれか?
  - データベースの作成と権限の付与
  - (スキーマおよび) テーブルの作成
- データベースにアクセスする際のアカウント・クレデンシャルは何か
