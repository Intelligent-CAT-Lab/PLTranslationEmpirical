WORKDIR=`pwd`
export PYTHONPATH=$WORKDIR;
export PYTHONIOENCODING=utf-8;

function prompt() {
    echo;
    echo "Syntax: bash scripts/clean_generations.sh MODEL DATASET";
    echo "MODEL: name of the model to use";
    echo "DATASET: name of the dataset to use";
    exit;
}

while getopts ":h" option; do
    case $option in
        h) # display help
          prompt;
    esac
done

if [[ $# < 2 ]]; then
  prompt;
fi

MODEL=$1;
DATASET=$2;

python3 src/translation/clean_generations.py --model $MODEL --dataset $DATASET;
