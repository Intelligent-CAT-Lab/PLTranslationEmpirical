import json
import os
import argparse
from pathlib import Path


def main(args):
    ordered_files = [x.strip() for x in open("evalplus_target_files.txt", "r").readlines()]
    os.makedirs(args.report_dir, exist_ok=True)
    compile_failed = []
    runtime_failed = []
    test_failed = []

    for f in ordered_files:

        fname = f + '.java'

        if os.path.exists(f'dataset/evalplus/evalplus_java/target/surefire-reports/com.example.{f}Test.txt'):
            with open(f'dataset/evalplus/evalplus_java/target/surefire-reports/com.example.{f}Test.txt', 'r') as report:
                content = report.read()
                if 'Errors: 0' not in content:
                    runtime_failed.append([fname, content])
                else:
                    test_failed.append([fname, content])

        elif f in []: # infinite loop
            runtime_failed.append([fname, 'the program enters an infinite loop'])

        else:
            os.system(f'javac dataset/evalplus/evalplus_java/src/main/java/com/example/{fname} 2> compile_out.txt')
            with open('compile_out.txt', 'r') as report:
                compile_failed.append([fname, report.read()])
            
            os.remove('compile_out.txt')

    json_fp = Path(args.report_dir).joinpath(f"{args.model}_evalplus_errors_from_{args.source_lang}_to_{args.target_lang}_{args.attempt}.json")
    with open(json_fp, "w", encoding="utf-8") as report:
        error_files = {'compile': compile_failed, 'runtime': runtime_failed, 'incorrect': test_failed}
        json.dump(error_files, report)
        report.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='execute evalplus tests')
    parser.add_argument('--source_lang', help='source language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--target_lang', help='target language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--model', help='model to use for code translation.', required=True, type=str)
    parser.add_argument('--report_dir', help='path to directory to store report', required=True, type=str)
    parser.add_argument('--attempt', help='attempt number', required=True, type=int)
    args = parser.parse_args()

    main(args)
