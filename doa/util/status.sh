# show status of Postgres Operator pods and services
set -e

echo "showing status of Postgres Operator services/pods..."
echo
kubectl get svc -l app.kubernetes.io/name=postgres-operator --show-kind
echo
kubectl get svc -l app.kubernetes.io/name=postgres-operator-ui --show-kind

echo
kubectl get pod -l app.kubernetes.io/name=postgres-operator --show-kind
echo 
kubectl get pod -l app.kubernetes.io/name=postgres-operator-ui --show-kind
