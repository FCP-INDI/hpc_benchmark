High Performance Computing (HPC) Benchmark
=============================================

Your friendly neighborhood lightweight utility for monitoring resource usage of your pipelines and analyses. <br>

Monitor metrics of any command line run. Metrics include CPU percentage, memory usage (MB), 
and processor information. Metrics information will be logged every second by default.
You can set the sampling rate with flag `--max_sampling_rate`. 
A CSV file will output after the run is complete that contains
metrics information. 
<br>

<b>Installation</b>
--------------------
Currently, this CLI tool is on TestPyPi.
To pip install: 
```
pip install -i https://test.pypi.org/simple/ hpc-benchmark
```

<b>User Guide</b>
------------------

<b>hpc_benchmark</b>

```
hpc_benchmark 'run command' [options] -o <output_directory>

Arguments:
    'run command'              Command line run you would like to monitor
    <output_directory>         Directory you would like to save output CSV file 

Options:
  --out_dir -o  PATH            Full path where output CSV file will be saved in
  --max_sampling_rate -msr INT  Frequency in seconds of how often to output metrics.
                                Default is about 1 second. This sampling rate is an 
                                estimate and may output +/- 2 seconds of the MSR.
  --help                        Print help
```

    INPUTS:
    - Your command should be between `' '`. This way, hpc_benchmark will run 
      whatever is between `' '` in the terminal.

    OUTPUTS:
    - Specify output directory with flag `-o`. hpc_benchmark will output a CSV file 
      with all the COU and memory usage informtion. 

    OPTIONAL: 
    - The `-msr INT` flag should be used if you want to specify the interval in which CPU 
      or memory usage gets benchmarked. It defaults to 1 second, so if you are running 
      something that takes hours, it is recommended to use `-msr 60` so that metric will 
      be meaured every minute.

EXAMPLE: 
```
hpc_benchmark 'docker run \
--security-opt=apparmor:unconfined \
--rm -v /home/{username}/data:/data \
-v /home/{username}/output:/output fcpindi/c-pac:latest \
/data /output participant \
--save_working_dir --skip_bids_validator \
--n_cpus 1 --mem_gb 15 \
--participant_label sub-12345 \
--preconfig abcd-options' \
-o /home/{username}/hpc_benchmark.csv -msr 60
```
<br> <br>
<b>hpc_plot_metrics</b>

```
hpc_plot_metrics </home/{username}/{file}.csv>

Arguments: 
  <CSV file>                  CSV file that was the output for hpc_benchmark run
```

Details: 
Use the output CSV file from your hpc_benchmark run as the input argument for 
hpc_plot_metrics. This will open a new tab in your internet browser of your plot. 
Plot can later be saved by clicking the camera icon in the top right corner.

EXAMPLE:
```
hpc_plot_metrics /home/{username}/hpc_benchmark.csv
```
![image](https://user-images.githubusercontent.com/58920810/225639070-fec2dc9d-ffdc-4603-937b-8a736ff71e5c.png)
