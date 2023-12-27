# Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code

[![Install](https://img.shields.io/badge/install-instructions-blue)](README.md#install)
[![Dependencies](https://img.shields.io/badge/install-dependencies-blue)](README.md#dependencies)
[![GitHub](https://img.shields.io/github/license/Intelligent-CAT-Lab/PLTranslationEmpirical?color=blue)](LICENSE)
[![Data](https://zenodo.org/badge/DOI/10.5281/zenodo.8190051.svg)](https://zenodo.org/doi/10.5281/zenodo.8190051)

Artifact repository for the paper [_Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code_](http://arxiv.org/abs/2308.03109), accepted at _ICSE 2024_, Lisbon, Portugal.
Authors are [Rangeet Pan][rangeet]* [Ali Reza Ibrahimzada][ali]*, [Rahul Krishna][rahul], Divya Sankar, Lambert Pougeum Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh Sinha, and [Reyhaneh Jabbarvand][reyhaneh].

[rangeet]: https://rangeetpan.github.io/
[ali]: https://alirezai.cs.illinois.edu/
[rahul]: http://rkrsn.us/
[reyhaneh]: https://reyhaneh.cs.illinois.edu/index.htm

### Install
This repository contains the source code for reproducing the results in our paper. Please start by cloning this repository:
```
git clone https://github.com/Intelligent-CAT-Lab/PLTranslationEmpirical
```

We recommend using a virtual environment for running the scripts. Please download `conda 23.11.0` from this [link](https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html). You can create a virtual environment using the following command:
```
conda create -n plempirical python=3.10.13
```

After creating the virtual environment, you can activate it using the following command:
```
conda activate plempirical
```

You can run the following command to make sure that you are using the correct version of Python:
```
python3 --version && pip3 --version
```

### Dependencies
To install all software dependencies, please execute the following command:
```
pip3 install -r requirements.txt
```

As for hardware dependencies, we used 16 NVIDIA A100 GPUs with 80GBs of memory for inferencing models. The models can be inferenced on any combination of GPUs as long as the reader can properly distribute the model weights across the GPUs. We did not perform weight distribution since we had enough memory (80 GB) per GPU.

Moreover, for compiling and testing the generated translations, we used Python 3.10, g++ 11, GCC Clang 14.0, Java 11, Go 1.20, Rust 1.73, and .Net 7.0.14 for Python, C++, C, Java, Go, Rust, and C#, respectively. Overall, we recommend using a machine with Linux OS and at least 32GB of RAM for running the scripts.

### Dataset
We uploaded the dataset we used in our empirical study to [Zenodo](https://zenodo.org/doi/10.5281/zenodo.8190051). The dataset is organized as follows:

1. [CodeNet](https://github.com/IBM/Project_CodeNet)
2. [AVATAR](https://github.com/wasiahmad/AVATAR)
3. [Evalplus](https://github.com/evalplus/evalplus)
4. [Apache Commons-CLI](https://github.com/apache/commons-cli)
5. [Click](https://github.com/pallets/click)

Please download and unzip the `dataset.zip` file from Zenodo. After unzipping, you should see the following directory structure:

```
PLTranslationEmpirical
├── dataset
    ├── codenet
    ├── avatar
    ├── evalplus
    ├── real-life-cli
├── ...
```

The structure of each dataset is as follows:

1. CodeNet & Avatar: Each directory in these datasets correspond to a source language where each include two directories `Code` and `TestCases` for code snippets and test cases, respectively. Each code snippet has an `id` in the filename, where the `id` is used as a prefix for test I/O files.

2. Evalplus: The source language code snippets follow a similar structure as CodeNet and Avatar. However, as a one time effort, we manually created the test cases in the target Java language inside a maven project, `evalplus_java`. To evaluate the translations from an LLM, we recommend moving the generated Java code snippets to the `src/main/java` directory of the maven project and then running the command `mvn clean test surefire-report:report -Dmaven.test.failure.ignore=true` to compile, test, and generate reports for the translations.

3. Real-life Projects: The `real-life-cli` directory represents two real-life CLI projects from Java and Python. These datasets only contain code snippets as files and no test cases. As mentioned in the paper, the authors manually evaluated the translations for these datasets.

### Scripts
We provide bash scripts for reproducing our results in this work. First, we discuss the translation script. For doing translation with a model and dataset, first you need to create a `.env` file in the repository and add the following:

```
OPENAI_API_KEY=<your openai api key>
LLAMA2_AUTH_TOKEN=<your llama2 auth token from huggingface>
STARCODER_AUTH_TOKEN=<your starcoder auth token from huggingface>
```

1. Translation with GPT-4: You can run the following command to translate all `Python -> Java` code snippets in `codenet` dataset with the `GPT-4` while top-k sampling is `k=50`, top-p sampling is `p=0.95`, and `temperature=0.7`:
```
bash scripts/translate.sh GPT-4 codenet Python Java 50 0.95 0.7 0
```

2. Translation with CodeGeeX: Prior to running the script, you need to clone the CodeGeeX repository from [here](https://github.com/THUDM/CodeGeeX) and use the instructions from their artifacts to download their model weights. After cloning it inside `PLTranslationEmpirical` and downloading the model weights, your directory structure should be like the following:

```
PLTranslationEmpirical
├── dataset
    ├── codenet
    ├── avatar
    ├── evalplus
    ├── real-life-cli
├── CodeGeeX
    ├── codegeex
    ├── codegeex_13b.pt # this file is the model weight
    ├── ...
├── ...
```

You can run the following command to translate all `Python -> Java` code snippets in `codenet` dataset with the `CodeGeeX` while top-k sampling is `k=50`, top-p sampling is `p=0.95`, and `temperature=0.2` on GPU `gpu_id=0`:
```
bash scripts/translate.sh CodeGeeX codenet Python Java 50 0.95 0.2 0
```

3. For all other models (StarCoder, CodeGen, LLaMa, TB-Airoboros, TB-Vicuna), you can execute the following command to translate all `Python -> Java` code snippets in `codenet` dataset with the `StarCoder|CodeGen|LLaMa|TB-Airoboros|TB-Vicuna` while top-k sampling is `k=50`, top-p sampling is `p=0.95`, and `temperature=0.2` on GPU `gpu_id=0`:
```
bash scripts/translate.sh StarCoder codenet Python Java 50 0.95 0.2 0
```

4. For compile and testing of CodeNet, AVATAR, and Evalplus (Python to Java) translations from GPT-4, and generating fix reports, you can run the following commands:
```
bash scripts/test_avatar.sh Python Java GPT-4 fix_reports 1
bash scripts/test_codenet.sh Python Java GPT-4 fix_reports 1
bash scripts/test_evalplus.sh Python Java GPT-4 fix_reports 1
```

5. For repairing unsuccessful translations of Java -> Python in CodeNet dataset with GPT-4, you can run the following commands:
```
bash scripts/repair.sh GPT-4 codenet Python Java 50 0.95 0.7 0 1 compile
bash scripts/repair.sh GPT-4 codenet Python Java 50 0.95 0.7 0 1 runtime
bash scripts/repair.sh GPT-4 codenet Python Java 50 0.95 0.7 0 1 incorrect
```

6. For cleaning translations of open-source LLMs (i.e., StarCoder) in codenet, you can run the following command:
```
bash scripts/clean_generations.sh StarCoder codenet
```
