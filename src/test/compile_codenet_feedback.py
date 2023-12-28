import os
import subprocess
import argparse
from subprocess import Popen, PIPE, STDOUT
import json
from pathlib import Path


def main(args):
    print('exporting reports')
    dataset = 'codenet'
    translation_dir = f"output/{args.model}/{dataset}/{args.source_lang}/{args.target_lang}"
    test_dir = f"dataset/{dataset}/{args.source_lang}/TestCases"
    os.makedirs(args.report_dir, exist_ok=True)
    files = [f for f in os.listdir(translation_dir) if f != '.DS_Store']

    compile_failed = []
    test_passed =[]
    test_failed =[]
    test_failed_details = []
    runtime_failed = []
    runtime_failed_details= []
    token_exceeded = []
    infinite_loop = []

    ordered_unsuccessful_fp = Path(args.report_dir).joinpath(f"{args.model}_{dataset}_compileReport_from_"+str(args.source_lang)+"_to_"+str(args.target_lang)+"_ordered_unsuccessful.txt")    
    ordered_files = [x.strip() for x in open(ordered_unsuccessful_fp, "r").readlines()]

    if args.target_lang =="Python":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("python3 -m py_compile "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=30)
                with open(test_dir+"/"+ files[i].split(".")[0]+"_in.txt" , 'r') as f:
                    f_in = f.read()
                f_out = open(test_dir+"/"+ files[i].split(".")[0]+"_out.txt", "r").read()

                p = Popen(['python3', translation_dir+"/"+ files[i]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    

                try:
                    stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                except subprocess.TimeoutExpired:
                    infinite_loop.append((files[i], "the program enters an infinite loop"))
                    continue

                if(stdout.decode(errors="ignore").strip()==f_out.strip()):
                    test_passed.append(files[i])
                else:
                    if stderr_data.decode()=='':
                        test_failed.append((files[i], f_in, f_out, stdout.decode(errors="ignore")))
                        test_failed_details.append('Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout.decode(errors="ignore")))  
                    else:
                        runtime_failed.append((files[i], stderr_data.decode()))
                        runtime_failed_details.append('Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode())) 

            except subprocess.CalledProcessError as exc:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], exc.stderr.decode()))

    elif args.target_lang =="Java":  # target language 
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("javac "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=30)
                with open(test_dir+"/"+ files[i].split(".")[0]+"_in.txt" , 'r') as f:
                    f_in = f.read()
                f_out = open(test_dir+"/"+ files[i].split(".")[0]+"_out.txt", "r").read()
                p = Popen(['java', files[i].split(".")[0]], cwd=translation_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)    

                try:
                    stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                except subprocess.TimeoutExpired:
                    infinite_loop.append((files[i], "the program enters an infinite loop"))
                    continue

                if(stdout.decode(errors="ignore").strip()==f_out.strip()): # stdout is from the translated code , f_out test data from original language 
                    test_passed.append(files[i])
                else:
                    if stderr_data.decode()=='':
                        test_failed.append((files[i], f_in, f_out, stdout.decode(errors="ignore")))
                        test_failed_details.append('Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout.decode(errors="ignore")))  
                    else:
                        runtime_failed.append((files[i], stderr_data.decode()))
                        runtime_failed_details.append('Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode())) 
            
            except subprocess.CalledProcessError as exc:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], exc.stderr.decode()))

        #remove all .class files generated
        dir_files = os.listdir(translation_dir)
        for fil in dir_files:
            if ".class" in fil: os.remove(translation_dir +"/"+ fil)

    elif args.target_lang == "C++":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("g++ -o exec_output -std=c++11 " + translation_dir+ "/"+ files[i], check=True, capture_output=True, shell=True)
                with open(test_dir+"/"+ files[i].split(".")[0]+"_in.txt" , 'r') as f:
                    f_in = f.read()
                f_out = open(test_dir+"/"+ files[i].split(".")[0]+"_out.txt", "r").read()
                p = Popen(['./exec_output'], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)    

                try:
                    stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                except subprocess.TimeoutExpired:
                    infinite_loop.append((files[i], "the program enters an infinite loop"))
                    continue

                if(stdout.decode(errors="ignore").strip()==f_out.strip()): # stdout is from the translated code , f_out test data from original language 
                    test_passed.append(files[i])
                else:
                    if stderr_data.decode()=='':
                        test_failed.append((files[i], f_in, f_out, stdout.decode(errors="ignore")))
                        test_failed_details.append('Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout.decode(errors="ignore")))  
                    else:
                        runtime_failed.append((files[i], stderr_data.decode()))
                        runtime_failed_details.append('Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode())) 

            except subprocess.CalledProcessError as exc:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], exc.stderr.decode()))

    elif args.target_lang == "C":
        for i in range(0,len(files)):
                
            if files[i] not in ordered_files:
                continue
            try:
                print('Filename: ', files[i])
                subprocess.run("gcc "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=10)
                with open(test_dir+"/"+ files[i].split(".")[0]+"_in.txt" , 'r') as f:
                    f_in = f.read()
                f_out = open(test_dir+"/"+ files[i].split(".")[0]+"_out.txt", "r").read()
                p = Popen(['./a.out'], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)    

                try:
                    stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                except subprocess.TimeoutExpired:
                    infinite_loop.append((files[i], "the program enters an infinite loop"))
                    continue

                if(stdout.decode(errors="ignore").strip()==f_out.strip()): # stdout is from the translated code , f_out test data from original language 
                    test_passed.append(files[i])
                else:
                    if stderr_data.decode()=='':
                        test_failed.append((files[i], f_in, f_out, stdout.decode(errors="ignore")))
                        test_failed_details.append('Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout.decode(errors="ignore")))  
                    else:
                        runtime_failed.append((files[i], stderr_data.decode()))
                        runtime_failed_details.append('Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode())) 

            except subprocess.CalledProcessError as exc:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], exc.stderr.decode()))

    elif args.target_lang == "Go":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("go build "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=30)
                with open(test_dir+"/"+ files[i].split(".")[0]+"_in.txt" , 'r') as f:
                    f_in = f.read()
                f_out = open(test_dir+"/"+ files[i].split(".")[0]+"_out.txt", "r").read()
                p = Popen(["./"+files[i].split(".")[0]], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)    

                try:
                    stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                except subprocess.TimeoutExpired:
                    infinite_loop.append((files[i], "the program enters an infinite loop"))
                    continue

                if(stdout.decode(errors="ignore").strip()==f_out.strip()): # stdout is from the translated code , f_out test data from original language 
                    test_passed.append(files[i])
                else:
                    if stderr_data.decode()=='':
                        test_failed.append((files[i], f_in, f_out, stdout.decode(errors="ignore")))
                        test_failed_details.append('Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout.decode(errors="ignore")))  
                    else:
                        runtime_failed.append((files[i], stderr_data.decode()))
                        runtime_failed_details.append('Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode())) 
                
            except subprocess.CalledProcessError as exc:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], exc.stderr.decode()))
                    print("Exception raised: ", exc)

            #remove generated files
            wd =  os.getcwd()
            if os.path.isfile(wd + "/" + files[i].split(".")[0]):
                os.remove(wd + "/" + files[i].split(".")[0])

    else:
        print("language:{} is not yet supported. select from the following languages[Python,Java,C,C++,Go]".format(args.target_lang))
        return

    attempt = args.attempt
    json_fp = Path(args.report_dir).joinpath(f"{args.model}_codenet_errors_from_{args.source_lang}_to_{args.target_lang}_{attempt}.json")
    with open(json_fp, "w", encoding="utf-8") as report:
        error_files = {'compile': compile_failed, 'runtime': runtime_failed + infinite_loop, 'incorrect': test_failed}
        json.dump(error_files, report)
        report.close()

    txt_fp = Path(args.report_dir).joinpath(f"{args.model}_codenet_errors_from_{args.source_lang}_to_{args.target_lang}_{attempt}.txt")
    report = open(txt_fp, 'w')
    for i in range(len(ordered_files)):
        if ordered_files[i] in [x[0] for x in compile_failed]:
            print("0,Compilation Error", file=report)
        elif ordered_files[i] in [x[0] for x in runtime_failed]:
            print("0,Runtime Error", file=report)
        elif ordered_files[i] in [x[0] for x in test_failed]:
            print("0,Wrong Output", file=report)
        elif ordered_files[i] in test_passed:
            print("1,Fixed", file=report)
        elif ordered_files[i] in token_exceeded:
            print("0,Token Exceeded", file=report)
        elif ordered_files[i] in [x[0] for x in infinite_loop]:
            print("0,Infinite Loop", file=report)
        else:
            print("0,Unknown", file=report)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='execute codenet tests')
    parser.add_argument('--source_lang', help='source language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--target_lang', help='target language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--model', help='args.model to use for code translation.', required=True, type=str)
    parser.add_argument('--report_dir', help='path to directory to store report', required=True, type=str)
    parser.add_argument('--attempt', help='attempt number', required=True, type=int)
    args = parser.parse_args()

    main(args)
