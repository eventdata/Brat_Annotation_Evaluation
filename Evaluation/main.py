#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: maryam
"""

import os
from glob import glob
import numpy as np
from ReadAnnotations import Ann2Json, EntityExactMatching, EntityPartialMatching, RelationPartialMatching, RelationExactMatching


def readAnnFiles (path2folder, matchingType, threshold ):
 
    entities = ['source', 'target', 'location', 'material_cooperation', 'material_conflict', 'verbal_cooperation', 'verbal_conflict']
    relations = ['srcAct','actTar']
    ent_rel = ['source', 'target', 'location', 'material_cooperation', 'material_conflict', 'verbal_cooperation', 'verbal_conflict', 'srcAct','actTar']

    folders = glob(path2folder)
    for goldFolder in folders:
        f1_score = list ()
        length = list()
        
        N_f1_score = list ()
        N_length = list()
        
        for folder in folders:
        
            if (goldFolder == folder):
                continue
            
            
            resultJson = { 'source':[],  'target':[], 'location':[], 'material_conflict':[], 'material_cooperation':[], 'verbal_cooperation':[], 'verbal_conflict':[], 'actTar':[], 'srcAct':[] }
            avgResultJson = { 'source':[],  'target':[], 'location':[], 'material_conflict':[], 'material_cooperation':[], 'verbal_cooperation':[], 'verbal_conflict':[], 'actTar':[], 'srcAct':[] }
            
            for filer in os.listdir(folder+'/'):
                if ('ann' in filer):                
                     
                    try:
                        goldJson= Ann2Json(goldFolder+'/'+filer)
                    except:
                        continue
                        pass 
                    
                    
                    try:
                        annotatorJson= Ann2Json(folder+'/'+filer)
                    except:
                        continue
                        pass
                    
                    for entity in entities:   
                        try:
                            if (matchingType == 'Exact'): 
                                resultJson[entity].append( EntityExactMatching(entity, goldJson, annotatorJson) )
                            else:
                                resultJson[entity].append( EntityPartialMatching(entity, goldJson, annotatorJson, threshold) )
                        except:
                            pass
                        
                    for relation in relations:
                        try:
                            if (matchingType == 'Exact'): 
                                resultJson[relation].append( RelationExactMatching(relation, goldJson, annotatorJson) )                                
                            else: 
                                resultJson[relation].append( RelationPartialMatching(relation, goldJson, annotatorJson, threshold) )
                        except:
                            pass

            print '==' * 50
            print 'Gold Standard:', goldFolder , 'VS ',  folder
            for er in ent_rel:
                avgResultJson[er] = np.mean(resultJson[er], axis=0)
                
                if ( len(resultJson[er]) != 0):
                    print er , len(resultJson[er]), avgResultJson[er]
                else:
                    avgResultJson[er] = [0,0,0]
                    print er , len(resultJson[er]), avgResultJson[er]
                
                f1_score.append(avgResultJson[er][2])
                length.append( len(resultJson[er]))
                
                
        print '--' * 50
        print 'Overall F1-score average for:', goldFolder
        print 'F1-score average:', np.mean(f1_score, axis=0)        
        print 'F1-score weighted average:', np.dot( f1_score, length) /sum(length)


if __name__ == '__main__':
    '''
    You can change the type of matching: Exact or Partial. 
    
    If you select Partial, you need to specify the threshold for string matching.
    '''
    
    # it is a path to the annotation folders
    path2folder = './protest_JJ/*'
    
    readAnnFiles (path2folder, matchingType = 'Partial', threshold= 75)
