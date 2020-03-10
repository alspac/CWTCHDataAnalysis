#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:27:34 2017

@authors: nicwells
"""

import os, csv
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
import CWTCHFunctions as cf

def get_parser():
    parser = ArgumentParser("CWTCH Join", description='Use to join Task and Completion data\
        output from CWTCHCompletionStatus and CWTCHQuestionnaireCompletion.')
    parser.add_argument('--input_task',required=True, help='Input task completion CWTCH')
    parser.add_argument('--input_quest',required=True, help='Input questionnaire completion CWTCH')
    parser.add_argument('--output',required=True, help='Output csv file path to write results to')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # get input file
    input_a = Path(args.input_task)
    if (not input_a.is_file()):
        print("Input file not found. Exiting...\n\n")
        quit()
    
    # get input file
    input_b = Path(args.input_quest)
    if (not input_b.is_file()):
        print("Input file not found. Exiting...\n\n")
        quit()
    
    # get output file
    output = Path(args.output)
    if (output.is_file()):
        print("Output file already exists. Exiting...\n\n")
        quit()
    
    # join inputs and write to output
    a = pd.read_csv(input_a,index_col='panelId')
    b = pd.read_csv(input_b,index_col='panelId')

    df = pd.merge(a,b,how='outer',on='panelId')
    df.index.name = 'panelId'
    df.to_csv(output, index=True) # output to csv
