#!/usr/bin/env python

import os
import subprocess
import pandas as pd
import numpy as np
import psutil
import nibabel as nb
import argparse
from subprocess import PIPE
import multiprocessing as mp
import time


def target(command):
    output = subprocess.run(command, check=True, capture_output=True, text=True).stdout
    print(output)


def log(command):
    output, sender = mp.Pipe(False)
    worker_process = mp.Process(target = target, args=(command,))
    worker_process.start()
    p = psutil.Process(worker_process.pid)

    log_time = []
    log_cpu = []
    log_mem = []

    while worker_process.is_alive():
        try:
            cpu = p.cpu_percent()
            ram = p.memory_info()[0]/1024/1024  # Convert from Bytes to MB
            for subproc in p.children(recursive=True):
                if not subproc.is_running():
                    continue
                subproc_dict = subproc.as_dict(attrs=['pid',
                                                    'name',
                                                    'cmdline',
                                                    'memory_info'])

                cpu += subproc.cpu_percent(interval=1)
                ram += subproc_dict['memory_info'][0] * ram_lut['B']

            tim = time.time()
            log_time.append(tim)
            log_cpu.append(cpu)
            log_mem.append(ram)
            time.sleep(0.05) #was 1

        except (psutil.AccessDenied,
                psutil.NoSuchProcess,
                TypeError, ValueError, AttributeError) as e:
            continue
    worker_process.join()

    log_time_asc=[]
    for i in range(len(log_time)):
        time_asc = time.asctime(time.localtime(log_time[i]))
        log_time_asc.append(time_asc)

    labels = ['LOG TIME', 'LOG CPU', 'LOG MEMORY']
    log_metrics = [np.array(log_time_asc), np.array(log_cpu), np.array(log_mem)]
    df = pd.DataFrame((np.array(log_metrics).T), columns = labels)
    return df    


def main():  
    parser = argparse.ArgumentParser()
    parser.add_argument('run_command', type=str, help='Command to benchmark')
    args = parser.parse_args()

    command = (str(args.run_command)).split(' ')
    output_df = log(command)

    out_path = os.path.join(os.getcwd(), 'run_metric_outputs.csv')
    df.to_csv(out_path, index = None)


if __name__ == '__main__':
    main()
