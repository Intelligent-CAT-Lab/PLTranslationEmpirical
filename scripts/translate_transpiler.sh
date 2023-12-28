WORKDIR=`pwd`
export PYTHONPATH=$WORKDIR;
export PYTHONIOENCODING=utf-8;

function prompt() {
    echo;
    echo "Syntax: bash scripts/translate_transpiler.sh DATASET SRC_LANG TRG_LANG TRANSPILER OUTPUT_DIR";
    echo "DATASET: name of the dataset to use";
    echo "SRC_LANG: source language";
    echo "TRG_LANG: target language";
    echo "TRANSPILER: name of the transpiler to use";
    echo "OUTPUT_DIR: path to the output directory";
    exit;
}

while getopts ":h" option; do
    case $option in
        h) # display help
          prompt;
    esac
done

if [[ $# < 5 ]]; then
  prompt;
fi

DATASET=$1;
SRC_LANG=$2;
TRG_LANG=$3;
TRANSPILER=$4;
OUTPUT_DIR=$5;

python3 src/translation/translate_transpiler.py --dataset $DATASET --source_lang $SRC_LANG --target_lang $TRG_LANG --transpiler $TRANSPILER --report_dir $OUTPUT_DIR;
