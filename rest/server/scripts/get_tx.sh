set -v
OUTFILE=$(mktemp --suffix=.json)
curl -X get -v localhost:8080/apps/day_trader/transaction -o ${OUTFILE}
type pbcopy >/dev/null 2>&1 && (echo "less ${OUTFILE}" | pbcopy)
