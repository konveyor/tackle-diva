#!/bin/bash
set -u

cyan() {
    echo $1
}

echo
cyan "------------------------"
cyan "DiVA-DOA v2.3.0"
cyan "------------------------"
echo

echo "DOA DB schema verifier"

# /app/doa: doa directory mounted
# /app/doa/verify.sh: this script
# /app/sql: SQL files

# ls -F --color /app/sql
n_files=$(find /app/sql -name "*.sql" | wc -l)
# echo "${n_files} SQL files"

# echo "connecting DB..."
# psql -c "\dt"

# no python env in the postgres image
# python -V 
# python3 -V

shopt -s globstar  # enable use of ** in filename patterns
IN_DIR=/app/sql
STAT_FILE=$1
VERBOSE=1

function normalscan() {
    # truncate -s 0 ${OUT_FILE}
    for sqlfile in ${IN_DIR}/**/*.sql; do
        # echo $(tput setaf 6)$sqlfile$(tput sgr setaf)
        # echo ${sqlfile}
        if [[ ${VERBOSE+x} ]]; then
            psql --set ON_ERROR_STOP=on -q -f $sqlfile
        else
            psql --set ON_ERROR_STOP=on -q -f $sqlfile >& /dev/null
        fi
        status_code=$?
        if [[ ${status_code} -ne 0 ]]; then 
            n_fail=$((${n_fail} + 1))
            echo ${sqlfile} >> ${STAT_FILE}
        fi
        if [[ ${status_code} -eq 0 ]]; then 
            n_success=$((${n_success} + 1))
        fi
    done
}


psql -c "create schema tqnet" > /dev/null
# psql -c "\dn"

echo "performing syntax verification..."
n_success=0
n_fail=0
truncate "${STAT_FILE}" -s 0
normalscan

# compute
perc_suc=$(echo "scale=2; ${n_success}*100/${n_files}" | bc)
perc_fail=$(echo "scale=2; ${n_fail}*100/${n_files}" | bc)

echo
echo "Number of converted SQLs for Postgres: ${n_files}"
echo "Syntax verification results:"
echo "  Success: ${n_success} (${perc_suc}%)"
echo "  Failure: ${n_fail} (${perc_fail}%)"

echo
echo "Number of PK/FK relationships: N/A"
echo "Semantics verification results:"
echo "  (skipped)"

echo
echo "detailed statistics ${STAT_FILE} has been generated."

echo
echo "[OK] verification completed."
