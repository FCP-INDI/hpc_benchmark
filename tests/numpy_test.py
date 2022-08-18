#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np
import time


def init_mat(N):
    return np.random.random((N, N))    


def sort_mat(mat):
    return np.sort(mat, kind="mergesort")


def iterate(lower, upper, delay):
    val = lower
    while val <= upper:
        print("Creating ({0}x{0}) matrix".format(val))
        tmp = init_mat(val)
        time.sleep(delay)
        print("Sorting matrix")
        tmp_sorted = sort_mat(tmp)
        time.sleep(delay)

        del tmp, tmp_sorted
        val *= 2


def main():
    parser = ArgumentParser(
        description="Will initialize matrices and wait a few seconds before "
                    "deleting them. The matrices will double in size from the "
                    "lower bound until the upper bound is reached.")
    parser.add_argument("lower", type=int,
                        help="Lower bound matrix size")
    parser.add_argument("upper", type=int,
                        help="Upper bound matrix size")
    parser.add_argument("--delay", "-d", type=float, default=0.3,
                        help="How long to hold a matrix (s)")

    args = parser.parse_args()
    iterate(args.lower, args.upper, args.delay)


if __name__ == "__main__":
    main()

