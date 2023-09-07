# main script. 
set -e
# set -x # for debugging

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
    echo "usage:"
    echo " ${APPNAME} -o <out_dir> <repo URL>"
}

cyan() {
    tput setaf 6 ; echo $1 ; tput sgr0
}

magenta() {
    tput setaf 5 ; echo $1 ; tput sgr0
}

# yellow
debug() {
    tput setaf 3 ; echo $1 ; tput sgr0
}

# green
ok() {
    tput setaf 2 ; echo $1 ; tput sgr0
}

# process optional arguments
while getopts o:i:l:fv OPT
do
    case $OPT in
        o) outdir=${OPTARG};;
        i) init_file=${OPTARG};;
        l) lang=${OPTARG};;
        f) files=1;;
        v) verbose=1;;
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
if [[ -n ${verbose+x} ]]; then
    echo "this script = $(readlink -f $0)"
    echo "pwd = $(pwd)"
    echo "base_dir = ${WORKDIR}"
    echo "use local files = ${files}"
    echo "repo URL (or directory) = ${REPO_URL}"
    echo "init_file (relative to repo dir) = ${init_file}"
    # echo "outdir (relative) = ${outdir}"
    echo "outdir (absolute) = ${OUTDIR}"
    echo "user id:"
    id
fi

# setup
echo 
cyan "setting up..."
mkdir -p "${OUTDIR}"

if [[ -z ${files+x} ]]; then
    # when "files" is not defined
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
else
    # when "files" is defined
    # debug "use local files"
    REPO_DIR="${REPO_URL}"
    APP_NAME="app"
    echo "application name = ${APP_NAME}"
fi

mkdir -p ${OUTDIR}/${APP_NAME}
OUTDIR=${OUTDIR}/${APP_NAME} # overwrite
# cyan "application directory ${OUTDIR} created."

echo
cyan "analyzing DBMS settings..."
# echo "analyzing configuration..."
# echo "analyzing credentials..."
DB_YAML=${OUTDIR}/postgresql.yaml
# echo "writing postgresql resource manifest to ${DB_YAML}..."
# cp ${WORKDIR}/manifests/postgresql.in.yaml ${DB_YAML}
jinja2 -D app_name=${APP_NAME} ${WORKDIR}/manifests/postgresql.in.yaml > ${DB_YAML}
echo "postgresql manifest $(tput setaf 5)${DB_YAML}$(tput sgr0) has been generated."

echo
cyan "analyzing SQL scripts..."
# debug "[under development]: invoking new version of analyzer..."
PYTHONPATH=${WORKDIR} python -m analyzers.analyze_sqls -n "${APP_NAME}" -i "${REPO_DIR}" -o "${OUTDIR}" ${lang+"-l"} ${lang}
# if [[ -f /tmp/out/stats.json ]]; then
#     mkdir -p "${OUTDIR}/stat"
#     cp /tmp/out/stats.json "${OUTDIR}/stat"
# fi

echo 
cyan "analyzing app start-up scripts..."
if [[ -n ${init_file+x} ]]; then
    init_file_opt="--init-file ${init_file}"
fi
PYTHONPATH=${WORKDIR} python -m analyzers.analyze_initdb -n "${APP_NAME}" -i "${REPO_DIR}" ${init_file_opt} -o "${OUTDIR}"

mkdir -p ${OUTDIR}/test
POD_YAML=${OUTDIR}/test/pod-test.yaml # Pod for test. To be removed in future.
JOB_YAML=${OUTDIR}/job-init.yaml
# echo "writing init Job manifest to ${JOB_YAML}..."
jinja2 -D app_name=${APP_NAME} ${WORKDIR}/manifests/job-init.in.yaml > ${JOB_YAML}
echo "job manifest (init job) $(tput setaf 5)${JOB_YAML}$(tput sgr0) has been generated."
jinja2 -D app_name=${APP_NAME} ${WORKDIR}/manifests/pod-test.in.yaml > ${POD_YAML}
echo "pod manifest (test pod) $(tput setaf 5)${POD_YAML}$(tput sgr0) has been generated."


echo 
cyan "post processing..."
DEPLOY_SH=${OUTDIR}/create.sh
# echo "generating deployment script to ${DEPLOY_SH}..."
cp ${WORKDIR}/create.sh ${DEPLOY_SH}
echo "deployment script $(tput setaf 5)${DEPLOY_SH}$(tput sgr0) has been generated."
DELETE_SH=${OUTDIR}/delete.sh
# echo "generating deployment script to ${DELETE_SH}..."
cp ${WORKDIR}/delete.sh ${DELETE_SH}
echo "undeployment script $(tput setaf 5)${DELETE_SH}$(tput sgr0) has been generated."

# all green
echo
ok "[OK] successfully generated manifest files."