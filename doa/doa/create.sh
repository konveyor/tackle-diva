# deploy generated manifests except for test Pod.
D=$(dirname $0)
kubectl apply -f "${D}"
