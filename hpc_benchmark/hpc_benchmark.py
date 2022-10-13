#!/usr/bin/env python

import os
import subprocess
import pandas as pd
import numpy as np
import psutil
import argparse
from subprocess import PIPE
import multiprocessing as mp
import time


def target(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print((output.strip()).decode())
    rc = process.poll()
    return rc


def log(command, timestep):
    output, sender = mp.Pipe(False)
    worker_process = mp.Process(target = target, args=(command,))
    worker_process.start()
    p = psutil.Process(worker_process.pid)

    log_time = []
    log_cpu = []
    log_mem = []
    log_nproc = []

    while worker_process.is_alive():
        try:
            cpu = p.cpu_percent()
            ram = p.memory_info()[0]/1024/1024  # Convert from Bytes to MB
            idx = 0
            for idx, subproc in enumerate(p.children(recursive=True)):
                if not subproc.is_running():
                    continue
                subproc_dict = subproc.as_dict(attrs=['pid',
                                                    'name',
                                                    'cmdline',
                                                    'memory_info'])

                cpu += subproc.cpu_percent(interval=1)
                ram += subproc_dict['memory_info'][0]/1024/1024

            tim = time.time()
            log_time.append(tim)
            log_cpu.append(cpu)
            log_mem.append(ram)
            log_nproc.append(idx+1)
            time.sleep(timestep)

        except (psutil.AccessDenied,
                psutil.NoSuchProcess,
                TypeError, ValueError, AttributeError) as e:
            continue
    worker_process.join()

    log_time_asc=[]
    for i in range(len(log_time)):
        time_asc = time.asctime(time.localtime(log_time[i]))
        log_time_asc.append(time_asc)
    
    labels = ['LOG TIME', 'LOG CPU', 'LOG MEMORY', 'LOG # PROC']
    log_metrics = [np.array(log_time_asc), np.array(log_cpu), np.array(log_mem), np.array(log_nproc)]
    df = pd.DataFrame((np.array(log_metrics).T), columns = labels)
    return df


def main():  
    parser = argparse.ArgumentParser(
        description = "Monitor any run in your command line. whatever you want to monitor (your commandline run) should be "
        " between ' ' and then whatever additional argument."   
    )
    parser.add_argument('run_command', type=str, help='Command to benchmark')
    parser.add_argument('--outdir', '-o', required = True, help='Directory of where output CSV should be saved. Default is it '
                        'will get saved in your current working directory')
    parser.add_argument('--max_sampling_rate', '-msr', default = 1, help='Frequency in seconds of how often to output metrics.'
                        'Default is about 1 second. This sampling rate is an estimate and may output +/- 2 seconds of the MSR.')
    args = parser.parse_args()

    outdir = (str(args.outdir))
    command = (str(args.run_command)).split(' ')
    timestep = (float(args.max_sampling_rate))
    output_df = log(command, timestep)

    if outdir is not None: 
        if os.path.splitext(outdir)[1] == '':
            out_path = os.path.join(outdir, 'run_metric_outputs.csv')
        else: 
            out_path = os.path.join(outdir)
            
    output_df.to_csv(out_path, index = None)


if __name__ == '__main__':
    main()
