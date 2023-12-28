import os
import subprocess
import json
from subprocess import Popen, PIPE
import argparse
from pathlib import Path


def main(args):
    print('exporting reports')    
    dataset = 'avatar'
    translation_dir = f"output/{args.model}/{dataset}/{args.source_lang}/{args.target_lang}"
    test_dir = f"dataset/{dataset}/{args.source_lang}/TestCases"
    files = [f for f in os.listdir(translation_dir) if f != '.DS_Store']

    compile_failed = []
    test_passed =[]
    test_failed =[]
    test_failed_details = []
    runtime_failed = []
    runtime_failed_details= []
    infinite_loop = []
    token_exceeded = []

    ordered_unsuccessful_fp = Path(args.report_dir).joinpath(f"{args.model}_{dataset}_compileReport_from_"+str(args.source_lang)+"_to_"+str(args.target_lang)+"_ordered_unsuccessful.txt")
    ordered_files = [x.strip() for x in open(ordered_unsuccessful_fp, "r").readlines()]

    if args.target_lang =="Python":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("python3 -m py_compile "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=30)

                tests_passed = 0
                for j in range(1000):

                    if os.path.exists(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in") == False:
                        if tests_passed == j:
                            test_passed.append(files[i])
                        
                        break

                    with open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in" , 'r') as f:
                        f_in = f.read()
                    f_out = open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.out", "r").read()
                    p = Popen(['python3', translation_dir+"/"+ files[i]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    

                    try:
                        stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                    except subprocess.TimeoutExpired:
                        infinite_loop.append((files[i], "the program enters an infinite loop"))
                        break

                    try:
                        if float(stdout.decode(errors="ignore"))%1 == 0:
                            stdout = str(int(float(stdout.decode(errors="ignore"))))
                            f_out = str(int(float(f_out)))
                        else:
                            # find how many decimal points are there in the output
                            stdout_temp = stdout.decode(errors="ignore").strip()
                            f_out_temp = f_out.strip()
                            f_out_total_dec_points = len(f_out_temp.split(".")[1])
                            stdout_total_dec_points = len(stdout_temp.split(".")[1])
                            min_dec_points = min(f_out_total_dec_points, stdout_total_dec_points)

                            stdout = str(round(float(stdout.decode(errors="ignore")), min_dec_points))
                            f_out = str(round(float(f_out), min_dec_points))

                    except:
                        if isinstance(stdout, bytes):
                            stdout = stdout.decode(errors="ignore")

                    if(stdout.strip()==f_out.strip()):
                        tests_passed+=1
                    else:
                        if stderr_data.decode()=='':
                            if files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))] and files[i] not in [test_failed[x][0] for x in range(len(test_failed))]:
                                test_failed.append((files[i], f_in, f_out, stdout))
                                test_failed_details.append('Test Index: '+str(j)+' Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout))
                        else:
                            if files[i] not in [test_failed[x][0] for x in range(len(test_failed))] and files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))]:
                                runtime_failed.append((files[i], stderr_data.decode()))
                                runtime_failed_details.append('Test Index: '+str(j)+' Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode()))

            except subprocess.CalledProcessError as e:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], e.stderr.decode()))

    elif args.target_lang =="Java":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("javac "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=30)

                tests_passed = 0
                for j in range(1000):

                    if os.path.exists(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in") == False:
                        if tests_passed == j:
                            test_passed.append(files[i])
                        
                        break

                    with open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in" , 'r') as f:
                        f_in = f.read()
                    f_out = open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.out", "r").read()
                    p = Popen(['java', files[i].split(".")[0]], cwd=translation_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)

                    try:
                        stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                    except subprocess.TimeoutExpired:
                        infinite_loop.append((files[i], "the program enters an infinite loop"))
                        break

                    try:
                        if float(stdout.decode(errors="ignore"))%1 == 0:
                            stdout = str(int(float(stdout.decode(errors="ignore"))))
                            f_out = str(int(float(f_out)))
                        else:
                            # find how many decimal points are there in the output
                            stdout_temp = stdout.decode(errors="ignore").strip()
                            f_out_temp = f_out.strip()
                            f_out_total_dec_points = len(f_out_temp.split(".")[1])
                            stdout_total_dec_points = len(stdout_temp.split(".")[1])
                            min_dec_points = min(f_out_total_dec_points, stdout_total_dec_points)

                            stdout = str(round(float(stdout.decode(errors="ignore")), min_dec_points))
                            f_out = str(round(float(f_out), min_dec_points))

                    except:
                        if isinstance(stdout, bytes):
                            stdout = stdout.decode(errors="ignore")

                    if(stdout.strip()==f_out.strip()):
                        tests_passed+=1
                    else:
                        if stderr_data.decode()=='':
                            if files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))] and files[i] not in [test_failed[x][0] for x in range(len(test_failed))]:
                                test_failed.append((files[i], f_in, f_out, stdout))
                                test_failed_details.append('Test Index: '+str(j)+' Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout))
                        else:
                            if files[i] not in [test_failed[x][0] for x in range(len(test_failed))] and files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))]:
                                runtime_failed.append((files[i], stderr_data.decode()))
                                runtime_failed_details.append('Test Index: '+str(j)+' Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode()))

            except subprocess.CalledProcessError as e:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], e.stderr.decode()))

        #remove all .class files generated
        dir_files = os.listdir(translation_dir)
        for fil in dir_files:
            if ".class" in fil: os.remove(translation_dir +"/"+ fil)

    elif args.target_lang == "C": 
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("gcc "+translation_dir+"/"+ files[i], check=True, capture_output=True, shell=True, timeout=10)

                tests_passed = 0
                for j in range(1000):

                    if os.path.exists(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in") == False:
                        if tests_passed == j:
                            test_passed.append(files[i])
                        
                        break

                    with open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in" , 'r') as f:
                        f_in = f.read()
                    f_out = open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.out", "r").read()
                    p = Popen(['./a.out'], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)

                    try:
                        stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                    except subprocess.TimeoutExpired:
                        infinite_loop.append((files[i], "the program enters an infinite loop"))
                        break

                    try:
                        if float(stdout.decode(errors="ignore"))%1 == 0:
                            stdout = str(int(float(stdout.decode(errors="ignore"))))
                            f_out = str(int(float(f_out)))
                        else:
                            # find how many decimal points are there in the output
                            stdout_temp = stdout.decode(errors="ignore").strip()
                            f_out_temp = f_out.strip()
                            f_out_total_dec_points = len(f_out_temp.split(".")[1])
                            stdout_total_dec_points = len(stdout_temp.split(".")[1])
                            min_dec_points = min(f_out_total_dec_points, stdout_total_dec_points)

                            stdout = str(round(float(stdout.decode(errors="ignore")), min_dec_points))
                            f_out = str(round(float(f_out), min_dec_points))

                    except:
                        if isinstance(stdout, bytes):
                            stdout = stdout.decode(errors="ignore")

                    if(stdout.strip()==f_out.strip()):
                        tests_passed+=1
                    else:
                        if stderr_data.decode()=='':
                            if files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))] and files[i] not in [test_failed[x][0] for x in range(len(test_failed))]:
                                test_failed.append((files[i], f_in, f_out, stdout))
                                test_failed_details.append('Test Index: '+str(j)+' Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout))
                        else:
                            if files[i] not in [test_failed[x][0] for x in range(len(test_failed))] and files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))]:
                                runtime_failed.append((files[i], stderr_data.decode()))
                                runtime_failed_details.append('Test Index: '+str(j)+' Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode()))

            except subprocess.CalledProcessError as e:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], e.stderr.decode()))

    elif args.target_lang == "C++":
        for i in range(0,len(files)):

            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("g++ -o exec_output -std=c++11 " + translation_dir + "/" + files[i], check=True, capture_output=True, shell=True, timeout=10)
                
                tests_passed = 0
                for j in range(1000):

                    if os.path.exists(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in") == False:
                        if tests_passed == j:
                            test_passed.append(files[i])
                        
                        break

                    with open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in" , 'r') as f:
                        f_in = f.read()
                    f_out = open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.out", "r").read()
                    p = Popen(['./exec_output'], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)

                    try:
                        stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                    except subprocess.TimeoutExpired:
                        infinite_loop.append((files[i], "the program enters an infinite loop"))
                        break

                    try:
                        if float(stdout.decode(errors="ignore"))%1 == 0:
                            stdout = str(int(float(stdout.decode(errors="ignore"))))
                            f_out = str(int(float(f_out)))
                        else:
                            # find how many decimal points are there in the output
                            stdout_temp = stdout.decode(errors="ignore").strip()
                            f_out_temp = f_out.strip()
                            f_out_total_dec_points = len(f_out_temp.split(".")[1])
                            stdout_total_dec_points = len(stdout_temp.split(".")[1])
                            min_dec_points = min(f_out_total_dec_points, stdout_total_dec_points)

                            stdout = str(round(float(stdout.decode(errors="ignore")), min_dec_points))
                            f_out = str(round(float(f_out), min_dec_points))

                    except:
                        if isinstance(stdout, bytes):
                            stdout = stdout.decode(errors="ignore")

                    if(stdout.strip()==f_out.strip()):
                        tests_passed+=1
                    else:
                        if stderr_data.decode()=='':
                            if files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))] and files[i] not in [test_failed[x][0] for x in range(len(test_failed))]:
                                test_failed.append((files[i], f_in, f_out, stdout))
                                test_failed_details.append('Test Index: '+str(j)+' Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout))
                        else:
                            if files[i] not in [test_failed[x][0] for x in range(len(test_failed))] and files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))]:
                                runtime_failed.append((files[i], stderr_data.decode()))
                                runtime_failed_details.append('Test Index: '+str(j)+' Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode()))

            except subprocess.CalledProcessError as e:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], e.stderr.decode()))

    elif args.target_lang == "Go":
        for i in range(0,len(files)):
            
            if files[i] not in ordered_files:
                continue

            try:
                print('Filename: ', files[i])
                subprocess.run("go build "+ translation_dir + "/" + files[i], check=True, capture_output=True, shell=True, timeout=30)
                
                tests_passed = 0
                for j in range(1000):

                    if os.path.exists(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in") == False:
                        if tests_passed == j:
                            test_passed.append(files[i])
                        
                        break

                    with open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.in" , 'r') as f:
                        f_in = f.read()
                    f_out = open(test_dir+"/"+ files[i].split(".")[0]+f"_{j}.out", "r").read()
                    p = Popen(["./"+files[i].split(".")[0]], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)    

                    try:
                        stdout, stderr_data = p.communicate(input=f_in.encode(), timeout=100)
                    except subprocess.TimeoutExpired:
                        infinite_loop.append((files[i], "the program enters an infinite loop"))
                        break

                    try:
                        if float(stdout.decode(errors="ignore"))%1 == 0:
                            stdout = str(int(float(stdout.decode(errors="ignore"))))
                            f_out = str(int(float(f_out)))
                        else:
                            # find how many decimal points are there in the output
                            stdout_temp = stdout.decode(errors="ignore").strip()
                            f_out_temp = f_out.strip()
                            f_out_total_dec_points = len(f_out_temp.split(".")[1])
                            stdout_total_dec_points = len(stdout_temp.split(".")[1])
                            min_dec_points = min(f_out_total_dec_points, stdout_total_dec_points)

                            stdout = str(round(float(stdout.decode(errors="ignore")), min_dec_points))
                            f_out = str(round(float(f_out), min_dec_points))

                    except:
                        if isinstance(stdout, bytes):
                            stdout = stdout.decode(errors="ignore")

                    if(stdout.strip()==f_out.strip()):
                        tests_passed+=1
                    else:
                        if stderr_data.decode()=='':
                            if files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))] and files[i] not in [test_failed[x][0] for x in range(len(test_failed))]:
                                test_failed.append((files[i], f_in, f_out, stdout))
                                test_failed_details.append('Test Index: '+str(j)+' Filename: '+files[i]+' Actual: '+str(f_out)+' Generated: '+ str(stdout))
                        else:
                            if files[i] not in [test_failed[x][0] for x in range(len(test_failed))] and files[i] not in [runtime_failed[x][0] for x in range(len(runtime_failed))]:
                                runtime_failed.append((files[i], stderr_data.decode()))
                                runtime_failed_details.append('Test Index: '+str(j)+' Filename: '+ files[i]+' Error_type: '+ str(stderr_data.decode()))

            except subprocess.CalledProcessError as e:
                if '# Token size exceeded.' in open(translation_dir+"/"+files[i], 'r').read():
                    token_exceeded.append(files[i])
                else:
                    compile_failed.append((files[i], e.stderr.decode()))

    else:
        print("language:{} is not yet supported. select from the following languages[Python,Java,C++,C,Go]".format(args.target_lang))
        return

    json_fp = Path(args.report_dir).joinpath(f"{args.model}_avatar_errors_from_{args.source_lang}_to_{args.target_lang}_{args.attempt}.json")
    with open(json_fp, "w", encoding="utf-8") as report:
        error_files = {'compile': compile_failed, 'runtime': runtime_failed + infinite_loop, 'incorrect': test_failed}
        json.dump(error_files, report)
        report.close()

    txt_fp = Path(args.report_dir).joinpath(f"{args.model}_avatar_errors_from_{args.source_lang}_to_{args.target_lang}_{args.attempt}.txt")
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

    parser = argparse.ArgumentParser(description='execute avatar tests')
    parser.add_argument('--source_lang', help='source language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--target_lang', help='target language to use for code translation. should be one of [Python,Java,C,C++,Go]', required=True, type=str)
    parser.add_argument('--model', help='model to use for code translation.', required=True, type=str)
    parser.add_argument('--report_dir', help='path to directory to store report', required=True, type=str)
    parser.add_argument('--attempt', help='attempt number', required=True, type=int)
    args = parser.parse_args()

    main(args)
