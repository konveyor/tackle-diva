# run diva-migrator container in Debian docker container.
# this script mounts the directory specified by -o

# Note for developers:
#   if you have "readlink -f" enabled, the following one-liner works:
#   docker run -it --rm -v $(readlink -f _out):/out diva-migrator:latest \
#       -o /out https://github.com/saud-aslam/trading-app

# ensure the given command sequence exists.
function ensure_command() {
    "$@" &> /dev/null && return 0
    echo -e "command \"$1\" not found. abort."
    exit 1
}

# $1: (relative) path of directory
# returned: absolute path
# status: not used
# Note: vanilla macOS does not have "-f" option to "readlink".
#       this only works on directory; cannot be used to files.
function abspath() {
    (cd $1 && pwd)
}

usage() {
    echo "usage: ${APPNAME} -o <out_dir> -i <init_file> -l <dialect> [-dfh] <repo URL>"
    echo
    echo "arguments:"
    echo "<repo URL>  Git repository URL of the target app."
    echo
    echo "options:"
    echo "-o  output directory (if does not exist, will be created) [default: ./output]"
    echo "-i  init_file that include DB init code"
    echo "-d  show debug messages including internal variables."
    echo "-l  dialect of SQL files to be processed. Currently only 'oracle' is supported."
    echo "-f  treat <repo URL> as a local directory name."
    echo "-h  show this help and exit."
    echo
}

# lookup required commands
ensure_command basename .
ensure_command dirname .

IMAGE=diva-doa:latest
APPNAME=$(basename $0)
WORKDIR=$(abspath $(dirname $0)) # this script's directory


# process optional arguments
while getopts dho:i:l:f OPT
do
    case $OPT in
        o) outdir=${OPTARG};;
        i) init_file=${OPTARG};;
        d) debug=1;;
        h) usage; exit 1;;
        l) lang=${OPTARG};;
        f) files=1;;
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

mkdir -p ${outdir:="./output"}
OUTDIR=$(abspath ${outdir})

# if files is defined, mount spcified directory to /in
if  [[ -n ${files+x} ]]; then
    files_flag="-v"
    files_mount="${REPO_URL}:/in"
    REPO_URL="/in"
fi

# if init_file is specified, turn the option on in docker run.
if [[ -n ${init_file+x} ]]; then
    init_file_opt="-i ${init_file}"
fi

echo "--------------------"
echo "DiVA-DOA wrapper"
echo "--------------------"

if [[ -n ${debug+x} ]]; then
    echo "* configurations:"
    echo "  this script = ${WORKDIR}/${APPNAME}"
    echo "  base_dir = ${WORKDIR}"
    echo "  pwd = $(pwd)"
    echo "  docker image to be run = ${IMAGE}"
    echo "* arguments:"
    echo "  repo URL = ${REPO_URL}"
    echo "  files = ${files}"
    echo "  SQL dialect = ${lang}"
    echo "  init_file (relative to repo dir) = ${init_file}"
    echo "  outdir (relative) = ${outdir}"
    echo "  outdir (absolute) = ${OUTDIR}"
fi


# main routine: run container and app with the output directory mounted.
# Note: OUTDIR should be absolute path. default "readlink" command of macOS 
#       does not have "-f" option, thus we provide a method abspath().
#       if you can use "readlink -f", you can use it instead.
echo
echo "running container ${IMAGE}..."
set -x
# need to specify "-l" (as login shell) to be able to execute locally installed Python module.
docker run -it --rm \
    -u vscode \
    -v ${OUTDIR}:/out \
    ${files_flag} ${files_mount} \
    ${IMAGE} \
    bash -l /work/migrate.sh -o /out ${init_file_opt} ${lang+"-l"} ${lang} ${files:+"-f"} ${REPO_URL} # arguments to migrate.sh in container
