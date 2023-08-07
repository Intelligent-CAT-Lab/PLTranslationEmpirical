# Programming Language Translation: An Empirical Study

### Compute Requirements

We used 16 NVIDIA A100 GPUs with 80GBs of memory for inferencing models. Moreover, for compiling and testing the generated translations, we used Python 3.10, g++ 11, GCC Clang 14.0, Java 11, and Go 1.20 for Python, C++, C, Java, and Go, respectively.

### Dependencies

To install all dependencies, please execute the following command:
```
pip3 install -r requirements.txt
```

### Dataset

We uploaded the dataset we used in our empirical study to [Zenodo](https://doi.org/10.5281/zenodo.8212996). The dataset is organized as follows:

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

Moreover, we provide manual labeling of translation bugs, vanilla generations of each model, and the generated repairs inside `artifacts.zip`.

### Prompts
1. GPT-4 Vanilla Prompt:
   ```
   $SOURCE_CODE

   # Translate the above $SOURCE_LANG code to $TARGET_LANG. Print only the $TARGET_LANG code and end with the comment "End of Code".
   ```

2. CodeGeeX Vanilla Prompt:
   ```
   code translation
   $SOURCE_LANG:
   $SOURCE_CODE
   
   $TARGET_LANG:
   ```
3. StarCoder, CodeGen, Llama-2, TheBloke-Airoboros, and TheBloke-Vicuna Vanilla Prompt:
   ```
   $SOURCE_LANG Code:
   $SOURCE_CODE

   Translate the above $SOURCE_LANG code to $TARGET_LANG.
   
   $TARGET_LANG Code:
   ```
4. GPT-4 Fix Prompt when effect is COMPILE ERROR or RUNTIME ERROR and dataset is Evalplus:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE
   
   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following error because it is syntactically incorrect:
   $STDERR

   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Print only the $TARGET_LANG code inside ```$TARGET_LANG{response}``` and do not add any other natural language description in your output, and do not change the method signature from incorrect translation. Make sure your generated code is syntactically correct.
   ```
5. GPT-4 Fix Prompt when effect is COMPILE ERROR or RUNTIME ERROR and dataset is CodeNet or AVATAR:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE

   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following error because it is syntactically incorrect:
   $STDERR
   
   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Print only the $TARGET_LANG code inside ```$TARGET_LANG{response}``` and do not add any other natural language description in your output. Make sure your generated code is syntactically correct.
   ```
6. GPT-4 Fix Prompt when effect is INCORRECT OUTPUT and dataset is Evalplus:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE
   
   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following test failure:
   $STDERR
   
   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Print only the $TARGET_LANG code inside ```$TARGET_LANG{response}```and do not add any other natural language description in your output, and do not change the method signature from incorrect translation. Make sure your generated code is syntactically correct."
   ```
7. GPT-4 Fix Prompt when effect is INCORRECT OUTPUT and dataset is CodeNet or AVATAR:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE
   
   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following output:
   $GENERATED_OUTPUT
   
   instead of the following expected output:
   $EXPECTED_OUTPUT
   
   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Print only the $TARGET_LANG code inside ```$TARGET_LANG{response}``` and do not add any other natural language description in your output. Make sure your generated code is syntactically correct. Your generated $TARGET_LANG code should take the following input and generate the expected output:
   
   Input:
   $TEST_INPUT
   
   Expected Output:
   $EXPECTED_OUTPUT
   ```
8. StarCoder, CodeGen, Llama-2 Fix Prompt when effect is COMPILE ERROR or RUNTIME ERROR and dataset is Evalplus:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE
   
   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following error because it is syntactically incorrect:
   $STDERR
   
   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Do not add any natural language description in your response, and do not change the method signature from incorrect translation.
   
   $TARGET_LANG Code:
   ```
9. StarCoder, CodeGen, Llama-2 Fix Prompt when effect is COMPILE ERROR or RUNTIME ERROR and dataset is CodeNet or AVATAR:
   ```
   You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
   $SOURCE_CODE
   
   Your response was the following $TARGET_LANG code:
   $TRANSLATED_CODE
   
   Executing your generated code gives the following error because it is syntactically incorrect:
   $STDERR
   
   Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Do not add any natural language description in your response.
   
   $TARGET_LANG Code:
   ```
10. StarCoder, CodeGen, Llama-2 Fix Prompt when effect is INCORRECT OUTPUT and dataset is Evalplus:
    ```
    You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
    $SOURCE_CODE
    
    Your response was the following $TARGET_LANG code:
    $TRANSLATED_CODE
    
    Executing your generated code gives the following test failure:
    $STDERR
    
    Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Do not add any natural language description in your output, and do not change the method signature from incorrect translation.
    
    $TARGET_LANG Code:
    ```
11. StarCoder, CodeGen, Llama-2 Fix Prompt when effect is INCORRECT OUTPUT and dataset is CodeNet or AVATAR:
    ```
    You were asked to translate the following $SOURCE_LANG code to $TARGET_LANG:
    $SOURCE_CODE
    
    Your response was the following $TARGET_LANG code:
    $TRANSLATED_CODE
    
    Executing your generated code gives the following output:
    $GENERATED_OUTPUT
    
    instead of the following expected output:
    $EXPECTED_OUTPUT
    
    Can you re-generate your response and translate the above $SOURCE_LANG code to $TARGET_LANG. Do not add any natural language description in your response. Your generated $TARGET_LANG code should take the following input and generate the expected output:
    
    Input:
    $TEST_INPUT
    
    Expected Output:
    $EXPECTED_OUTPUT
    
    $TARGET_LANG Code:
    ```

Note 1: For StarCoder, the prompt is encapsulated inside special tokens `<fim_prefix>` and `<fim_suffix><fim_middle>`.

Note 2: We consider Non-terminating Execution (NTE) effect as a RUNTIME ERROR and replace the STDERR with a custom feedback "the program enters infinite loop".

### Appendix
TO BE ADDED

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
