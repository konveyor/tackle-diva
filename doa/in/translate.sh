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
    echo "  ${APPNAME} [-v] -f -l <lang> [-o <out_dir>] <in_dir>"
}

cyan() {
    tput setaf 6 ; echo $1 ; tput sgr0
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
    echo "verbose = ${verbose}"
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
# cyan "analyzing SQL scripts..."
PYTHONPATH=${WORKDIR} python -m analyzers.convert -n "${APP_NAME}" -i "${REPO_DIR}" -o "${OUTDIR}" ${lang+"-l"} ${lang}
# if [[ -f /tmp/out/stats.json ]]; then
#     mkdir -p "${OUTDIR}/stat"
#     cp /tmp/out/stats.json "${OUTDIR}/stat"
# fi

# all green
# echo
# ok "[OK] translation successfully completed."