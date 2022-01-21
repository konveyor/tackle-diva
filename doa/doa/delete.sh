# delete created resources with manifests.
D=$(dirname $0)
kubectl delete -f "${D}"
