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
    parser = ArgumentParser("CWTCH Questionnaire Completed", description='Use to convert questionnaire json file downloaded from CWTCH\
        Cognitive Tasks Ounce web application to a csv file containing completion information for participants.')
    parser.add_argument('--input',required=True, help='Input json file of task results from CWTCH')
    parser.add_argument('--output',required=True, help='Output csv file path to write results to')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # get input file
    input = Path(args.input)
    if (not input.is_file()):
        print("Input file not found. Exiting...\n\n")
        quit()
    
    # get output file
    output = Path(args.output)
    if (output.is_file()):
        print("Output file already exists. Exiting...\n\n")
        quit()
    
    # Load data
    jsonData = cf.loadData(input)

    # Remove blank entries and check size matches
    jsonData = [x for x in jsonData if x]    

    participantQuestStatus = {}

    # Iterate participant questionnaire data
    for index, participantData in enumerate(jsonData):
        for q in participantData:
            panelId = q['pid'] # participant username
            hasQuestionnaire = False
            if 'questionnaire' in q:
                # has some questionnaire data
                hasQuestionnaire = True
                
            panel = {
                'hasQuestionnaire': hasQuestionnaire
            }
            # add new entry into participants dict
            participantQuestStatus[panelId] = panel
 
    # convert participants dict to dataframe
    df = pd.DataFrame.from_dict(participantQuestStatus, orient='index')
    df.index.name = 'panelId'

    df.to_csv(output, index=True) # output to csv

    print("Ouput written to {}".format(output))
    
