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
    parser = ArgumentParser("CWTCH Tasks Completed", description='Use to convert json file downloaded from CWTCH\
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

    participantTaskStatus = {}

    # Iterate participant task data
    for index, participantData in enumerate(jsonData):
        for task in participantData:
            panelId = task['panelId'] # participant username
            taskName = task['taskId'] # task name (oddity or spatial)
            state = task['state'] # completion status

            panel = None

            # see if participant already exists in dict
            if panelId in participantTaskStatus:
                # retrieve existing dict object and append task data to it
                panel = participantTaskStatus[panelId]
                panel[(taskName+"_taskStatus")] = state
                # update dict of participants
                participantTaskStatus[panelId] = panel
            else:
                # create dict object for participant
                # with task and state of this json object
                panel = {
                    (taskName+"_taskStatus"): state
                }
                # add new entry into participants dict
                participantTaskStatus[panelId] = panel
 
    # convert participants dict to dataframe
    df = pd.DataFrame.from_dict(participantTaskStatus, orient='index')
    df.index.name = 'panelId'

    # add column to indicate if completed everything
    df['completed_both_tasks'] = (df['spatial_taskStatus'] == 'completed') & (df['oddity_taskStatus'] == 'completed')

    df.to_csv(output, index=True) # output to csv

    print("Ouput written to {}".format(output))
    
