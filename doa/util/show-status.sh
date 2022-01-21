# show status of Postgres Operator pods and services
set -e

echo "showing minikube status..."
echo
minikube status

echo "showing kubectl status..."
echo
kubectl cluster-info

echo
echo "Helm version..."
echo
helm version

echo
echo "showing Helm charts..."
echo
helm list --filter 'postgres-operator'

echo
echo "showing status of Postgres Operator services/pods..."
echo
kubectl get svc -l "app.kubernetes.io/name in (postgres-operator, postgres-operator-ui)" --show-kind
echo
kubectl get pod -l "app.kubernetes.io/name in (postgres-operator, postgres-operator-ui)" --show-kind
