#!/usr/bin/env python
"""
Plot CPU percentage and memory usage from the hpc_benchmark ouput CSV file.  
Usage:
    hpc_plot_metrics <run_metrics.csv>

Arguments:
    <run_metrics.csv>          Output CSV file from running hpc_benchmark

DETAILS
Use the output CSV file from your hpc_benchmark run as the input argument for 
hpc_plot_metrics. This will open a new tab in your internet browser of your plot. 
Plot can later be saved by clicking the camera icon in the top right corner. 

Written by Amy Gutierrez (amy.gutierrez@childmind.org)
"""

#import argparse
import sys
import pandas as pd
import click
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@click.command()
@click.argument('file', required=True)
def plot(file):
    #parser = argparse.ArgumentParser()
    #parser.add_argument('file', help='CSV file from hpc_benchmark')
    #args = parser.parse_args()

    one_file = str(file)

    data = pd.read_csv (one_file, header = 0)
    df = pd.DataFrame(data)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['LOG TIME'], y=df['LOG CPU'], name="LOG CPU"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['LOG TIME'], y=df['LOG MEMORY'], name="LOG MEMORY"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="LOG CPU & MEMORY"
    )

    fig.update_xaxes(title_text="TIME")

    fig.update_yaxes(title_text="LOG CPU (%)", secondary_y=False)
    fig.update_yaxes(title_text="LOG MEMORY (MB)", secondary_y=True)

    fig.show()
    
    return