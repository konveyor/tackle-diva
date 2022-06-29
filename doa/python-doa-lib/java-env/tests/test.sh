#!/bin/bash
set -eu
shopt -s globstar

basedir=$(readlink -f $(dirname $0)/..) # project root 
plsql_java=$(readlink -f ${basedir}/plsql-java/clz)
export CLASSPATH="${plsql_java}:${CLASSPATH}"

for i in $(seq 0 15)
do
    tput setaf ${i} && echo "color ${i}"
done 

tput setaf 11 && echo "Note: input files are conveted to uppercase and passed to the parser." && tput sgr0 
echo ""

for testcase in ${basedir}/tests/*.sql
do
    echo "processing $(tput setaf 14)${testcase}$(tput sgr0)..."
    echo ""

    cat ${testcase} | tr [:lower:] [:upper:] | java org.antlr.v4.gui.TestRig PlSql unit_statement -tree
    echo ""
done