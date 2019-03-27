#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import zipfile,fnmatch
from subprocess import call
from filelock import SoftFileLock, Timeout
import polymer
import random
from polymer.main import run_atm_corr, Level1, Level2
from polymer.level2 import default_datasets,OutputExists

# root folder of data
folder = "/spectral/gaobing/inputfile/" 

# file containing list of data files to run
fname = folder + "2018unzipfilelist.txt" 

# algorithm created by user
def user_algorithm(filename);
    run_atm_corr(Level1(filename), Level2(outdir="/spectral/gaobing/OLCI/done_2019", fmt='netcdf4', datasets=default_datasets+['SPM']), multiprocessing=-1 )


# code to handle concurreny is below
# 
# 
completed_fn = folder + "completed_2019_old.txt"
completed_lockname = folder + "completed_2019_old.txt.lock"
prcessing_fn = folder + "processing_2019_old.txt"
prcessing_lockname = folder + "processing_2019_old.txt.lock"

def test():
    tic=time.clock()
    count=0
    with open(fname, "r") as f:
        lines = f.readlines()
        input_len = number_of_lines(fname)
        while count < input_len/4:
            random_line=random.choice(lines)
            print("file is ", random_line)
            found_in_comp = check_file_status(completed_fn,random_line)
            found_in_proc = check_file_status(prcessing_fn,random_line )
            if (found_in_comp == False and found_in_proc == False):
                process_images(random_line)
                count = count+1
                clean_up(random_line)
    print("process file count", count)        
    toc=time.clock()
    print('Total processing time: (seconds)')
    print(toc-tic)

def number_of_lines(filename):
    with open(filename, "r") as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def check_file_status(filename,random_line):

    logfile = open(str(filename), 'r')
    loglist = logfile.readlines()
    logfile.close()
    found = False
    for line in loglist:
        if str(random_line) in line:
            print ("Found it")
            found = True
    return found  

def clean_up( random_line):

    lock = SoftFileLock(completed_lockname, timeout=35)
    with lock:
        try:
            with lock.acquire(timeout=30):
                print("lock acquired - complete_file")
                with open(completed_fn, 'a') as outfile: outfile.write(random_line)
        except Timeout:
            print("timed out - complete_file")
            time.sleep(5)


def process_images( random_line):
    conflict = 0;
    tic=time.clock()
    filepath= str(random_line).replace('/home/gaobing/projects/rpp-ycoady/spectral','/spectral',1)
    #filename = line.rsplit('/',1)[1].strip()
    filename = filepath.strip()
# level2 filename determined from level1 name, if outdir is not provided it will go to the same folder as level1
# for fn in glob(filepath+pattern ,recursive=True):
    print("new file name is ",filename)
    lock = SoftFileLock(prcessing_lockname, timeout=45)
    with lock:
        try:
            with lock.acquire(timeout=35):
                with open(prcessing_fn, 'a') as outfile: outfile.write(random_line)
        except Timeout:
            print("timed out - prcessing_fn")
            time.sleep(5)
    try:
        user_algorithm(filename)
    except OutputExists:
        print("found this one exists in destination")
        conflict = conflict+1
        return     
    toc=time.clock()
    print('Processing time for images',random_line,': (seconds)')
    print(toc-tic)
    print('conflict number ', conflict)

test()
