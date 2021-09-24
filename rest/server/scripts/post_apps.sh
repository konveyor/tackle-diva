set -v
curl -X post -i -H "content-type: application/json" -d @$(dirname $0)/apps.json localhost:8080/apps
