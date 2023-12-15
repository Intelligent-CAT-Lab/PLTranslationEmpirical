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
