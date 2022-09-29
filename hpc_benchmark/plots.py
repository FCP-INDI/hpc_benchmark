import argparse
import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Input CSV file from hpc_benchmark')
args = parser.parse_args()

one_file = (str(args.file))

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

fig.update_yaxes(title_text="LOG CPU", secondary_y=False)
fig.update_yaxes(title_text="LOG MEMORY", secondary_y=True)

fig.show()