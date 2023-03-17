#!/usr/bin/env python
"""
Monitor CPU percetage, memory in MB, and processor information of any command line run
Usage:
    hpc_benchmark 'run command' [options] <output_directory>

Arguments:
    'run command'              Command line run you would like to monitor
    <output_directory>         Directory you would like to save output CSV file 

Options:
  --out_dir -o  PATH            Full path where output CSV file will be saved in
  --max_sampling_rate -msr INT  Frequency in seconds of how often to output metrics.
                                Default is about 1 second. This sampling rate is an 
                                estimate and may output +/- 2 seconds of the MSR.
  --help                        Print help
DETAILS
Monitor metrics of any command line run. Metrics include CPU percentage, memory usage (MB), 
and processor information. Metrics information will be logged every second by default.
You can set the sampling rate with flag `--max_sampling_rate`. 
A CSV file will output after the run is complete that contains
metrics information. 

Written by Amy Gutierrez (amy.gutierrez@childmind.org)
"""

import os
import subprocess
import pandas as pd
import numpy as np
import psutil
from subprocess import PIPE
import multiprocessing as mp
import time
import click


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


@click.command()
@click.argument('run_command', type=click.STRING, required=True)
@click.option('--outdir', '-o', required=True, help='Directory of where output CSV should be saved')
@click.option('--max_sampling_rate', '-msr', default=1, help='Frequency in seconds of how often to output metrics.'
            'Default is about 1 second. This sampling rate is an estimate and may output +/- 2 seconds of the MSR.')
def run(run_command, outdir=None, max_sampling_rate=None):  

    command = str(run_command).split(' ')
    timestep = float(max_sampling_rate)
    output_df = log(command, timestep)

    if outdir is not None: 
        if os.path.splitext(outdir)[1] == '':
            out_path = os.path.join(outdir, 'run_metric_outputs.csv')
        else: 
            out_path = os.path.join(outdir)
            
    output_df.to_csv(out_path, index = None)
    return
