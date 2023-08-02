WORKDIR=`pwd`
export PYTHONPATH=$WORKDIR;
export PYTHONIOENCODING=utf-8;

function prompt() {
    echo;
    echo "Syntax: bash scripts/repair.sh MODEL DATASET SRC_LANG TRG_LANG K P TEMPERATURE GPU_ID ATTEMPT ERROR_TYPE";
    echo "MODEL: name of the model to use";
    echo "DATASET: name of the dataset to use";
    echo "SRC_LANG: source language";
    echo "TRG_LANG: target language";
    echo "K: top-k sampling";
    echo "P: top-p sampling";
    echo "TEMPERATURE: temperature for sampling";
    echo "GPU_ID: GPU to use";
    echo "ATTEMPT: attempt number";
    echo "ERROR_TYPE: type of error to repair. must be one of: 'compile', 'runtime', 'incorrect'";
    exit;
}

while getopts ":h" option; do
    case $option in
        h) # display help
          prompt;
    esac
done

if [[ $# < 10 ]]; then
  prompt;
fi

MODEL=$1;
DATASET=$2;
SRC_LANG=$3;
TRG_LANG=$4;
K=$5;
P=$6;
TEMPERATURE=$7;
GPU_ID=$8;
ATTEMPT=$9;
ERROR_TYPE=${10};

if [[ $MODEL == "GPT-4" || $MODEL == "StarCoder" || $MODEL == "CodeGen" || $MODEL == "CodeGeeX" || $MODEL == "LLaMa" || $MODEL == "TB-Airoboros" || $MODEL == "TB-Vicuna" ]]; then
  python3 src/translation/repair.py --model $MODEL --dataset $DATASET --source_lang $SRC_LANG --target_lang $TRG_LANG --k $K --p $P --temperature $TEMPERATURE --gpu_id $GPU_ID --attempt $ATTEMPT --error_type $ERROR_TYPE;
else
  echo "Model not supported";
fi
