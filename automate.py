"""
Calling from a subdirectory will result in core dump
"""

import subprocess
import pickle
import os

def run_program():
    os.chdir("../cacti/")
    result = subprocess.run(["./cacti", "-infile", "../model-cacti/tmp.cfg"], \
                          check=False, capture_output=True, encoding="utf8")
    os.chdir("../model-cacti")
    return result

def set_cache_size(lines, cache_size):
    line1 = lines[1].split()
    line1[-1] = str(cache_size)+'\n'
    lines[1] = " ".join(line1)

def set_cache_asso(lines, asso):
    line2 = lines[2].split()
    line2[-1] = str(asso)+'\n'
    lines[2] = " ".join(line2)
    #if asso == 0:
    #    lines[4] = "-search port 1\n" # how many search ports?
    #else:
    #    lines[4] = "\n"

def parse_results(olines):
    d = dict()
    d["access_time"] = float(olines[57].split(':')[-1])
    d["cycle_time"] = float(olines[58].split(':')[-1])
    d["dyn_read"] = float(olines[59].split(':')[-1])
    d["dyn_write"] = float(olines[60].split(':')[-1])
    d["leakage"] = float(olines[61].split(':')[-1])
    d["gate_leakage"] = float(olines[62].split(':')[-1])
    return d

def d2list(d):
    try:
        ret = [d["access_time"], d["cycle_time"], d["dyn_read"], d["dyn_write"], d["leakage"], d["gate_leakage"]]
    except KeyError:
        ret = [0,0,0,0,0,0]
    return ret

f = open("ref.cfg",'r')
lines = f.readlines()
results = list()
associativities = [1, 2, 4]
cache_size_list = [base*m for base in [2**i for i in range(9,17)] for m in range(4,8)]
for associativity in associativities:
    print(associativity)
    for cache_size in cache_size_list:
        print("#",end='',flush=True)
        set_cache_size(lines, cache_size)
        set_cache_asso(lines, associativity)
        f_out = open("tmp.cfg", 'w')
        f_out.writelines(lines)
        f_out.close()
        run_result = run_program()
        if run_result.returncode != 0:
            result = {}
        else:
            olines = run_result.stdout.split('\n')
            result = parse_results(olines)
        results.append([associativity, cache_size] + d2list(result))
    print("")
f_p = open("results.pkl",'wb')
pickle.dump(results, f_p)
f_p.close()