# test for creating a ConfigMap.
TMPDIR=$(mktemp -d)
CM_NAME=one-cm-from-multi-files
CM_YAML=${CM_NAME}.yaml

echo "CONFIG:"
echo ${TMPDIR}
echo ${CM_NAME}
echo ${CM_YAML}
echo 

rm -rf /tmp/out

mkdir -p ${TMPDIR}/a
mkdir -p ${TMPDIR}/b
echo '-- test sql file (1)' > ${TMPDIR}/a/c.sql
echo '-- test sql file (2)' > ${TMPDIR}/b/d.sql

python ./analyze_sqls.py -i ${TMPDIR} --app-name myapp
echo $?

ls -alF /tmp/out
