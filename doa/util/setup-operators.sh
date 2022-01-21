# install Postgres Operator and UI.

set -e # abort on failure

kubectl cluster-info &> /dev/null || (echo "[ERROR] k8s cluster is not ready. abort."; exit 1)
echo "kubectl is installed."

which -s helm || (echo "helm is not installed. abort."; exit 2)
echo "helm is installed."

CURDIR=$(dirname $0)
which -s tput && tput_found=1

debug() {
    if [[ -v tput_found ]]; then
        tput setaf 3; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

echo
debug "installing Postgres Operators to \"default\" namespace..."
TEMP_DIR=`mktemp -d`
git clone https://github.com/zalando/postgres-operator.git ${TEMP_DIR}

debug "installing postgres-operator..."
helm install postgres-operator ${TEMP_DIR}/charts/postgres-operator
debug "installing postgres-operator-ui..."
helm install postgres-operator-ui ${TEMP_DIR}/charts/postgres-operator-ui

echo
debug "installed. following Operator Services are installed:"
echo
kubectl get svc -l "app.kubernetes.io/name in (postgres-operator, postgres-operator-ui)"
