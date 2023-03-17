import sys
import click
from cli.bin import run
from cli.bin import plot

@click.group(help="CLI tool to sutomate CPAC regression tests")

def main():
    pass

main.add_command(run.run)
main.add_command(plot.plot)

if __name__ == '__main__':
    fig = main()
    sys.exit(fig)