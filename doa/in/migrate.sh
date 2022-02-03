# main script. 
set -e

APPNAME=$(basename $0)
WORKDIR=$(readlink -f $(dirname $0)) # this script's directory

# check if colored output is enabled
which tput >/dev/null && tput_found=1
if [[ -v tput_found ]]; then
    bold=$(tput bold)
    unbold=$(tput sgr bold)
else
    bold=""
    unbold=""
fi

usage() {
    echo "usage: ${APPNAME} -o <out_dir> <repo URL>"
}

cyan() {
    tput setaf 6 ; echo $1 ; tput sgr0
}

debug() {
    tput setaf 3 ; echo $1 ; tput sgr0
}

ok() {
    tput setaf 2 ; echo $1 ; tput sgr0
}

# process optional arguments
while getopts o:i: OPT
do
    case $OPT in
        o) outdir=${OPTARG};;
        i) init_file=${OPTARG};;
        \?) exit 1;;
    esac
done

# process positional argument
shift $((OPTIND-1))
if (($#==0)); then
    usage
    exit 1
fi
REPO_URL=$1

# set other variables
OUTDIR=$(readlink -f ${outdir})

# log
echo
cyan "------------------------"
cyan "DiVA-DOA v{{version}}"
cyan "------------------------"
echo "this script = $(readlink -f $0)"
echo "pwd = $(pwd)"
echo "base_dir = ${WORKDIR}"
echo "repo URL = ${REPO_URL}"
echo "init_file (relative to repo dir) = ${init_file}"
echo "outdir (relative) = ${outdir}"
echo "outdir (absolute) = ${OUTDIR}"
echo "user id:"
id

# setup
echo 
cyan "setting up..."
mkdir -p "${OUTDIR}"
REPO_DIR=`mktemp -d`
echo "REPO_DIR = ${REPO_DIR}"
echo "directory for repository created: ${REPO_DIR}"

# main routine

# clone repo
echo
cyan "cloning repository..."
git clone ${REPO_URL} ${REPO_DIR}

echo
cyan "analyzing application..."
APP_NAME=${REPO_URL##*/} # pick up segment after the last "/"
echo "application name = ${APP_NAME}"

echo
cyan "analyzing DBMS settings..."
echo "analyzing configuration..."
echo "analyzing credentials..."
DB_YAML=${OUTDIR}/${APP_NAME}-postgres.yaml
echo "writing postgresql resource manifest to ${DB_YAML}..."
cp ${WORKDIR}/manifests/database.yaml ${DB_YAML}

echo
cyan "analyzing SQL scripts..."
# debug "[under development]: invoking new version of analyzer..."
PYTHONPATH=${WORKDIR} python -m analyzers.analyze_sqls -n "${APP_NAME}" -i "${REPO_DIR}" -o "${OUTDIR}"

echo 
cyan "analyzing app start-up scripts..."
PYTHONPATH=${WORKDIR} python -m analyzers.analyze_initdb -n "${APP_NAME}" -i "${REPO_DIR}" --init-file "${init_file}" -o "${OUTDIR}"

mkdir -p ${OUTDIR}/test
POD_YAML=${OUTDIR}/test/${APP_NAME}-pod-init.yaml # Pod for test. To be removed in future.
JOB_YAML=${OUTDIR}/${APP_NAME}-job-init.yaml
echo "writing init Job manifest to ${JOB_YAML}..."
cp ${WORKDIR}/manifests/pod-init.yaml ${POD_YAML}
cp ${WORKDIR}/manifests/job-init.yaml ${JOB_YAML}

echo 
cyan "post processing..."
DEPLOY_SH=${OUTDIR}/create.sh
echo "generating deployment script to ${DEPLOY_SH}..."
cp ${WORKDIR}/create.sh ${DEPLOY_SH}
DELETE_SH=${OUTDIR}/delete.sh
echo "generating deployment script to ${DELETE_SH}..."
cp ${WORKDIR}/delete.sh ${DELETE_SH}

# all green
echo
ok "[OK] successfully completed."
