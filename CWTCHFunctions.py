#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  14 15:31:31 2017

@author: mattjones
"""


## This file contains all of the functions used in the CWTCH Analysis Script (CWTCHAnalysisScript.py)

#%% The loadData function is used to load the json data file.  It can contain mulitple subjects.
def loadData( filename ):

    import json

    with open(filename) as data_file:
        jsondata = json.load(data_file)

    assert isinstance(jsondata, object)
    return jsondata

#%% The loadParticipant function is used to extract all data for a single subject.
def loadParticipant( alljsondata, participantid ):
    
    participantdata = alljsondata[participantid]
    
    return participantdata

#%% The getTaskData function is used to extract the individual tasks from the subject's data.
def getTaskData ( participantdata, taskid ):
    
    taskdata = next((item for item in participantdata if item["taskId"] == taskid), 'None')
  
    return taskdata

#%% this function processes the data trial-by-trial and produces a flattened list to return back to the main script
def processData (data):
    
    completeddata = [] # creates an empty list to store the trial data
    
    # the following if statement looks to see the task-type
    if data['taskId'] == 'oddity':
        
        phaseData = data['phases']
                
        # get general data
        participantId = data['panelId']
        datetimeStarted = data['created']
        
        # this loop runs through each phase and flattens the data
        for phaseNo, phase in enumerate(phaseData):
    
            kind = phase['phase']['kind']
            condition = phase['phase']['type']
            block = phase['blocks']
            # this if statement is added as I wasnt sure if there was always  
            # only one entry in the 'block' list just created. So its just an
            # error check.
            if len(block) == 1: 
                phaseStartTime = block[0]['startBlock']
                phaseEndTime = block[0]['endBlock']
                trials = block[0]['trials']
                # the following loop runs through and flattens the trial by 
                # trial data and then appends it to the completeddata list.
                for trialNo, trial in enumerate(trials):
                        trialStartTime = trial['startTrial']
                        trialEndTime = trial['endTrial']
                        stimulus = trial['stimulus']
                        clickedTime = trial['clicked']
                        correct = trial['location'][3]
                        # populate dictionary entry
                        entry = {}
                        entry['participantID'] = participantId
                        entry['datetimeStarted'] = datetimeStarted
                        entry['phaseNo'] = phaseNo
                        entry['kind'] = kind
                        entry['condition'] = condition
                        entry['phaseStartTime'] = phaseStartTime
                        entry['phaseEndTime'] = phaseEndTime
                        entry['trialNo'] = trialNo
                        entry['trialStartTime'] = trialStartTime
                        entry['trialEndTime'] = trialEndTime
                        entry['stimulus'] = stimulus
                        entry['clickedTime'] = clickedTime
                        entry['correct'] = correct
                        #add to list
                        completeddata.append(entry)
            else:
                exit("oddity length of block is greater than one - something wrong!")
         
    elif data['taskId'] == 'spatial':
        
        phaseData = data['phases']
                
        # get general data
        participantId = data['panelId']
        datetimeStarted = data['created']
        
        # this loop runs through each phase and flattens the data
        for phaseNo, phase in enumerate(phaseData):
    
            kind = phase['phase']
            phaseStartTime = phase['startPhase']
            trials = phase['blocks'][0]['trials']
            # the following loop runs through and flattens the trial by 
            # trial data and then appends it to the completeddata list.
            for trialNo, trial in enumerate(trials):
                scndresp = bool(0) # this resets the boolean value that tells the loop below which response it s.
                trialStartTime = trial['startTrial']
                trialEndTime = trial['endTrial']
                condition = trial['condition']
                set1 = trial['set'][0]
                set2 = trial['set'][1]
                set3 = trial['set'][2]
                stimuli = trial['stimuli']

                # the following loop and if statements runs through each each 
                # stimuli in the trial and looks to see if it is correct or not.
                # It looks a bit complicated because it needs to check whether 
                # the trial contains two possible targets or just one.
                for index, stimulus in enumerate(stimuli):
                    if set3 == 6:
                        if scndresp is bool(0):
                            if 'isTarget' in stimulus.keys():
                                targetItem1 = (index)
                                scndresp = bool(1)
                                if 'clicked' in stimulus.keys():
                                    response1 = bool(1)
                                    rt1 = stimulus['clicked']
                                else:
                                    response1 = bool(0)
                                    rt1 = float('nan')
                        elif scndresp is bool(1):
                            if 'isTarget' in stimulus.keys():
                                targetItem2 = (index)
                                if 'clicked' in stimulus.keys():
                                    response2 = bool(1)
                                    rt2 = stimulus['clicked']
                                else:
                                    response2 = bool(0)
                                    rt2 = float('nan')
                    elif set3 == 7:
                        if 'isTarget' in stimulus.keys():
                            targetItem1 = (index)
                            targetItem2 = float('nan')
                            if 'clicked' in stimulus.keys():
                                response1 = bool(1)
                                rt1 = stimulus['clicked']
                                response2 = float('nan')
                                rt2 = float('nan')
                            else:
                                response1 = bool(0)
                                rt1 = float('nan')
                                response2 = float('nan')
                                rt2 = float('nan')
                                
                # the following loop and if statements run through the stimuli
                # in each trial (regardless of whether there were 6 or 7 unique
                # items presented) and checks if the participant clicked despite
                # a target not being presented (i.e. false alarm).
                falseAlarms = [] # create an empty list to store data for false alarms
                
                for index, stimulus in enumerate(stimuli):
                    if 'clicked' in stimulus.keys():
                        if 'isTarget' not in stimulus.keys():
                            falseAlarms.append(1)
                totalFalseAlarms = sum(falseAlarms)
                        
                # populate dictionary entry
                entry = {}
                entry['participantID'] = participantId
                entry['datetimeStarted'] = datetimeStarted
                entry['phaseNo'] = phaseNo
                entry['phase'] = kind
                entry['condition'] = condition
                entry['phaseStartTime'] = phaseStartTime
                entry['trialNo'] = trialNo
                entry['trialStartTime'] = trialStartTime
                entry['trialEndTime'] = trialEndTime
                entry['set1'] = set1
                entry['set2'] = set2
                entry['set3'] = set3
                entry['stimulus'] = stimulus['item']
                entry['targetItem1'] = targetItem1
                entry['response1'] = response1
                entry['rt1'] = rt1
                entry['targetItem2'] = targetItem2
                entry['response2'] = response2
                entry['rt2'] = rt2
                entry['totalFalseAlarms'] = totalFalseAlarms
                #add to list
                completeddata.append(entry)
           
    return completeddata
 
#%% This function is used to transform and flatten the list data into a pandas dataframe
def flattenData ( data ):
    import pandas as pd
    a = pd.DataFrame()
    for participant in data:
        a = a.append(participant)
        
    return a
        
