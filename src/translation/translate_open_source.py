import os
import logging
from dotenv import load_dotenv
import time
import argparse
from tqdm import tqdm
import torch
import codegeex
from codegeex.tokenizer import CodeGeeXTokenizer
from codegeex.torch import CodeGeeXModel
from transformers import AutoTokenizer, AutoModelForCausalLM


os.makedirs(f'logs', exist_ok=True)
logging.basicConfig(filename=f"logs/translation.log", level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def main(args):

    extensions = { 'Python': 'py','C': 'c','C++': 'c++','Java': 'java','Go': 'go', "Rust": "rs", "C#": "cs" }

    in_folder = f'dataset/{args.dataset}/{args.source_lang}/Code'
    out_folder = f'output/{args.model}/{args.dataset}/{args.source_lang}/{args.target_lang}'

    in_files = os.listdir(in_folder)
    print(f'found {len(in_files)} inputs')

    # check for files alraedy extracted
    already_extracted_files = []
    if os.path.exists(out_folder):
        already_extracted_files = os.listdir(out_folder)
        if len(already_extracted_files) > 0:
            already_extracted_files = [x.split('.')[0] for x in already_extracted_files if os.stat(f'{out_folder}/{x}').st_size != 0]

    if len(already_extracted_files) > 0:
        in_files = [x for x in in_files if x.split('.')[0] not in already_extracted_files]

    ext = extensions[args.target_lang]
    device = f'cuda:{args.gpu_id}'

    tokenizer, model = None, None
    if args.model == 'CodeGeeX':
        tokenizer = CodeGeeXTokenizer(
            tokenizer_path=os.getcwd() + "/CodeGeeX/codegeex/tokenizer/",
            mode="codegeex-13b")

        state_dict = torch.load(os.getcwd() + "/CodeGeeX/codegeex_13b.pt", map_location="cpu")
        state_dict = state_dict["module"]

        model = CodeGeeXModel(hidden_size=5120, num_layers=39, num_attention_heads=40, padded_vocab_size=52224, max_position_embeddings=2048)
        model.load_state_dict(state_dict)
        model.eval()
        model.half()
        torch.cuda.set_device(device)
        model.cuda()
        torch.cuda.synchronize()

    elif args.model == 'StarCoder':
        tokenizer = AutoTokenizer.from_pretrained('bigcode/starcoder', use_auth_token=os.environ['STARCODER_AUTH_TOKEN'], cache_dir='./huggingface')
        model = AutoModelForCausalLM.from_pretrained('bigcode/starcoder', use_auth_token=os.environ['STARCODER_AUTH_TOKEN'], cache_dir='./huggingface').to(device)
    elif args.model == 'CodeGen':
        kwargs = {}
        kwargs["torch_dtype"] = torch.float16
        tokenizer = AutoTokenizer.from_pretrained('Salesforce/codegen-16B-multi', cache_dir='./huggingface')
        model = AutoModelForCausalLM.from_pretrained('Salesforce/codegen-16B-multi', cache_dir='./huggingface', **kwargs).to(device)
    elif args.model == 'LLaMa':
        tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-13b-chat-hf', use_auth_token=os.environ['LLAMA2_AUTH_TOKEN'], cache_dir='./huggingface')
        model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-13b-chat-hf', use_auth_token=os.environ['LLAMA2_AUTH_TOKEN'], cache_dir='./huggingface').to(device)
    elif args.model == 'TB-Airoboros':
        tokenizer = AutoTokenizer.from_pretrained('TheBloke/airoboros-13B-HF', cache_dir='./huggingface')
        model = AutoModelForCausalLM.from_pretrained('TheBloke/airoboros-13B-HF', cache_dir='./huggingface').to(device)
    elif args.model == 'TB-Vicuna':
        tokenizer = AutoTokenizer.from_pretrained('TheBloke/Wizard-Vicuna-13B-Uncensored-HF', cache_dir='./huggingface')
        model = AutoModelForCausalLM.from_pretrained('TheBloke/Wizard-Vicuna-13B-Uncensored-HF', cache_dir='./huggingface').to(device)
    
    # loop over input files
    os.makedirs(out_folder, exist_ok=True)
    for f in tqdm(in_files):
        prompt_file = f'{in_folder}/{f}'

        with open(prompt_file, "r", encoding="ISO-8859-1", errors='ignore') as fin:
            prompt = fin.readlines()

            if args.model == 'CodeGeeX':
                prompt = f"code translation\n{args.source_lang}:\n" + "".join(prompt) + f'\n\n{args.target_lang}:\n'
            elif args.model == 'StarCoder':
                prompt = f"{args.source_lang} Code:\n\n" + "".join(prompt) + f'\n\nTranslate the above {args.source_lang} code to {args.target_lang}.\n\n{args.target_lang} Code:\n\n'
                prefix_token = "<fim_prefix>"
                suffix_token = "<fim_suffix><fim_middle>"
                prompt = prefix_token + prompt + suffix_token
            elif args.model == 'CodeGen':
                prompt = f"{args.source_lang} Code:\n\n" + "".join(prompt) + f'\n\nTranslate the above {args.source_lang} code to {args.target_lang}.\n\n{args.target_lang} Code:\n\n'
            elif args.model == 'LLaMa':
                prompt = f"{args.source_lang} Code:\n\n" + "".join(prompt) + f'\n\nTranslate the above {args.source_lang} code to {args.target_lang}.\n\n{args.target_lang} Code:\n\n'
            elif args.model == 'TB-Airoboros':
                prompt = f"{args.source_lang} Code:\n\n" + "".join(prompt) + f'\n\nTranslate the above {args.source_lang} code to {args.target_lang}.\n\n{args.target_lang} Code:\n\n'
            elif args.model == 'TB-Vicuna':
                prompt = f"{args.source_lang} Code:\n\n" + "".join(prompt) + f'\n\nTranslate the above {args.source_lang} code to {args.target_lang}.\n\n{args.target_lang} Code:\n\n'

            try:
                t0 = time.perf_counter()

                inputs = []
                if args.model == 'CodeGeeX':
                    inputs = tokenizer.encode_code(prompt)
                    inputs = torch.tensor(inputs).reshape(1, len(inputs)).to(device)
                else:
                    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)

                total_input_tokens = inputs.shape[1]
                model_max_length = 4096 if args.model == 'LLaMa' else 2048
                if total_input_tokens >= model_max_length:
                    out_file = f'{out_folder}/{f.split(".")[0]}.{ext}'
                    with open(out_file, 'w') as fot:
                        print("# Token size exceeded.", file=fot)
                    continue
                max_new_tokens = model_max_length - total_input_tokens

                raw_outputs = ''
                if args.model == 'CodeGeeX':
                    raw_outputs = codegeex.generate(
                        model,
                        tokenizer,
                        prompt,
                        out_seq_length=max_new_tokens,
                        seq_length=2048,
                        top_k=args.k,
                        top_p=args.p,
                        temperature=args.temperature,
                        micro_batch_size=1,
                        backend="megatron",
                        verbose=True,
                    )
                
                else:
                    raw_outputs = model.generate(
                        inputs,
                        max_new_tokens=max_new_tokens,
                        do_sample=True,
                        top_p=args.p,
                        top_k=args.k,
                        temperature=args.temperature,
                        repetition_penalty=1,
                        pad_token_id=tokenizer.eos_token_id,
                    )


                t1 = time.perf_counter()
                print("Total generation time:", t1 - t0)
                out_file = f'{out_folder}/{f.split(".")[0]}.{ext}'                
                with open(out_file, 'w') as fot:
                    if args.model == 'CodeGeeX':
                        for g in raw_outputs:
                            fot.write(g)
                    else:
                        print(tokenizer.decode(raw_outputs[0]), file=fot)

            except (ValueError, FileNotFoundError) as e:
                print(e)
                continue


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='run translation with open-source models given dataset and languages')
    parser.add_argument('--model', help='model to use for code translation. should be one of [CodeGeeX,StarCoder,CodeGen,TB-Airoboros,TB-Vicuna,LLaMa]', required=True, type=str)
    parser.add_argument('--dataset', help='dataset to use for code translation. should be one of [codenet,avatar,evalplus]', required=True, type=str)
    parser.add_argument('--source_lang', help='source language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--target_lang', help='target language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--k', help='The number of highest probability vocabulary tokens to keep for top-k-filtering. Only applies for sampling mode, with range from 1 to 100.', required=True, type=int)
    parser.add_argument('--p', help='Only the most probable tokens with probabilities that add up to top_p or higher are considered during decoding. The valid range is 0.0 to 1.0. 1.0 is equivalent to disabled and is the default. Only applies to sampling mode. Also known as nucleus sampling.', required=True, type=float)
    parser.add_argument('--temperature', help='A value used to warp next-token probabilities in sampling mode. Values less than 1.0 sharpen the probability distribution, resulting in "less random" output. Values greater than 1.0 flatten the probability distribution, resulting in "more random" output. A value of 1.0 has no effect and is the default. The allowed range is 0.0 to 2.0.', required=True, type=float)
    parser.add_argument('--gpu_id', help='gpu id to use', required=True, type=int)
    args = parser.parse_args()

    # Initialize configurations
    source = args.source_lang
    target = args.target_lang
    logging.info(f"translating examples from {source} to {target} using {args.model} and {args.dataset} dataset")
    main(args)
