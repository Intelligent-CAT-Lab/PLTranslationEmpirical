"""
We used a simple heuristic to clean the generations of the open-source models. Feel free to play with the extraction
heuristic to get better results.
"""

import os
import re
import argparse

def list_files(startpath):
    files = []
    for root, dirs, walkfiles in os.walk(startpath):
        for name in walkfiles:
            files.append(os.path.join(root, name))

    return files


def clean_codegeex(dataset):
    main_path = f'output/CodeGeeX/{dataset}'
    output_path = 'output/CodeGeeX/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()

        valid_lines = []
        for line in data.split('\n'):
            if line.strip() in ['C:', 'C++:', 'Java:', 'Python:', 'Go:', '"""']:
                break
            else:
                valid_lines.append(line)
        
        data = '\n'.join(valid_lines)
        data = data.replace('<|endoftext|>', '')
        data = data.replace(f'```{target_lang.lower()}', '')
        data = data.replace(f'```', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)
        
        if target_lang == 'Java' and dataset == 'evalplus':
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)


def clean_codegen(dataset):
    main_path = f'output/CodeGen/{dataset}'
    output_path = 'output/CodeGen/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()

        data = data[data.find(f'{target_lang} Code:')+len(f'{target_lang} Code:'):].strip()        

        valid_lines = []
        for line in data.split('\n'):
            if line.strip() in ["*/", 'C Code:', 'C++ Code:', 'Java Code:', 'Python Code:', 'Go Code:']:
                break
            else:
                valid_lines.append(line)
        
        data = '\n'.join(valid_lines)
        data = data.replace('<|endoftext|>', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)

        if target_lang == 'Java' and dataset == 'evalplus' and 'package com.example;' not in data:
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)



def clean_starcoder(dataset):
    main_path = f'output/StarCoder/{dataset}'
    output_path = 'output/StarCoder/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()
        
        data = data[data.find('<fim_suffix><fim_middle>')+len('<fim_suffix><fim_middle>'):]

        valid_lines = []
        for line in data.split('\n'):
            if line.strip() in ["'''", 'C Code:', 'C++ Code:', 'Java Code:', 'Python Code:', 'Go Code:', '"""'] or line.strip().startswith("Input") or line.strip().startswith("Output"):
                break
            else:
                valid_lines.append(line)
        
        data = '\n'.join(valid_lines)
        data = data.replace('<|endoftext|>', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)

        if target_lang == 'Java' and dataset == 'evalplus' and 'package com.example;' not in data:
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)


def clean_llama(dataset):
    main_path = f'output/LLaMa/{dataset}'
    output_path = 'output/LLaMa/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()

        data = data[data.find(f'{target_lang} Code:')+len(f'{target_lang} Code:'):].strip()

        valid_lines = []
        for line in data.split('\n'):
            if line.strip().startswith("Sure"):
                continue
            if line.strip().startswith("Please") or line.strip().startswith("Note") or line.strip().startswith("Here") or line.strip().startswith("In"):
                break
            else:
                valid_lines.append(line)
        
        data = '\n'.join(valid_lines)

        data = data.replace('</s>', '')
        data = data.replace(f'```{target_lang.lower()}', '')
        data = data.replace(f'```', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)

        if target_lang == 'Java' and dataset == 'evalplus' and 'package com.example;' not in data:
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)


def clean_airoboros(dataset):
    main_path = f'output/TB-Airoboros/{dataset}'
    output_path = 'output/TB-Airoboros/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()

        data = data[data.find(f'{target_lang} Code:')+len(f'{target_lang} Code:'):].strip()

        data = data.replace('</s>', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)

        if target_lang == 'Java' and dataset == 'evalplus':
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)


def clean_vicuna(dataset):
    main_path = f'output/TB-Vicuna/{dataset}'
    output_path = 'output/TB-Vicuna/'

    files = list_files(main_path)

    for f in files:

        splitted = f.split('/')
        filename = splitted[-1].strip()
        target_lang = splitted[-2].strip()
        source_lang = splitted[-3].strip()

        with open(f, 'r') as file:
            data = file.read()

        data = data[data.find(f'{target_lang} Code:')+len(f'{target_lang} Code:'):].strip()

        valid_lines = []
        for line in data.split('\n'):
            if line.strip().startswith("Translate the above") or line.strip().startswith("Note:") or line.strip().startswith("What is"):
                break
            else:
                valid_lines.append(line)
        
        data = '\n'.join(valid_lines)

        data = data.replace('</s>', '')

        if target_lang == 'Java':
            data = re.sub('public\s*class\s*.+', 'public class ' + filename.split('.')[0] + ' {', data)

        if target_lang == 'Java' and dataset == 'evalplus':
            data = 'package com.example;\n' + data

        os.makedirs(output_path + dataset + '/' + source_lang + '/' + target_lang, exist_ok=True)
        with open(output_path + dataset + '/' + source_lang + '/' + target_lang + '/' + filename, 'w') as file:
            file.write(data)


def main(args):

    if args.model == 'CodeGeeX':
        clean_codegeex(args.dataset)
    elif args.model == 'StarCoder':
        clean_starcoder(args.dataset)
    elif args.model == 'LLaMa':
        clean_llama(args.dataset)
    elif args.model == 'CodeGen':
        clean_codegen(args.dataset)
    elif args.model == 'TB-Airoboros':
        clean_airoboros(args.dataset)
    elif args.model == 'TB-Vicuna':
        clean_vicuna(args.dataset)    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='clean open-source model generations given a dataset and a model')
    parser.add_argument('--model', help='model to use for code translation. should be one of [GPT-4,LLaMa,StarCoder,CodeGen,TB-Airoboros,TB-Vicuna]', required=True, type=str)
    parser.add_argument('--dataset', help='dataset to use for code translation. should be one of [codenet,avatar,evalplus,real-life-cli]', required=True, type=str)
    args = parser.parse_args()
    main(args)
