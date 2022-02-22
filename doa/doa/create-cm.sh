# creates a CM for SQL scripts.
# copied from terminal. not tested yet.
kubectl create cm trading-app-init --from-file=../psql/trading_ddl/
