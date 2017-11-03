#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Created on Fri Jul 28 11:54:42 2017

@author: maryam
'''
import json
import sys
from fuzzywuzzy import fuzz

#reload(sys)
#sys.setdefaultencoding('utf-8')


def Ann2Json(fileName):
    JsonFile = { "source":[],  'target':[], 'location':[], 'material_conflict':[], 'material_cooperation':[], 'verbal_cooperation':[], 'verbal_conflict':[], 'actTar':[], 'srcAct':[] }
    
    dic = dict()
    with open (fileName, 'r') as f: 
        for line in f.readlines():
            if line.strip() =='':
                continue
            
            try:
                line_parts = line.strip().split('\t')
                
                if line[0] == 'T':
                    tag = line_parts[1].split()[0]
                    index = ' '.join(line_parts[1].split()[1:])
                    phrase = line_parts[-1].strip()
                    dic[line_parts[0]] = [tag, index, phrase]
                    
                    JsonFile[tag].append({'inx': index , 'phrase': phrase}) 
                    
                elif line[0] == 'R':
                    tag = line_parts[1].split()[0]
                    Arg1 = dic[ line_parts[1].split(' ')[1].split(':')[1] ]
                    Arg2 = dic[ line_parts[1].split(' ')[2].split(':')[1] ]
                    dic[line_parts[0]] = [tag, Arg1, Arg2]
                    
                    JsonFile[tag].append({'Arg1': Arg1 , 'Arg2': Arg2 }) 
                else :
                    continue
            except: 
                pass
    return json.dumps(JsonFile)


def EntityExactMatching(tag, goldJson, annotatorJson):
    
    '''
    doing the exact match
    '''
    tp , fp , fn = 0, 0, 0
    
    tag_parts_Gold = json.loads(goldJson)[tag]
    tag_parts = json.loads(annotatorJson)[tag]
    
    Gold = list()
    annotator = list()
    
    if (len(tag_parts_Gold)== 0 or len(tag_parts)==0):
        raise Exception('Empty')
    
    for g in tag_parts_Gold:
        if g not in Gold:
            Gold.append(g)
    
    for g in tag_parts:
        if g not in annotator:
            annotator.append(g)
    
    for tag_part_Gold in tag_parts_Gold:
        for tag_part in tag_parts: 
            
            if ( tag_part not in annotator or tag_part_Gold not in Gold):
                continue
            
            if (';' not in tag_part_Gold['inx'] and ';' not in tag_part['inx']):
                [start_inx_Gold, end_inx_Gold] = [int(i) for i in tag_part_Gold['inx'].split() ]
                [start_inx, end_inx] = [int(i) for i in tag_part['inx'].split() ]
                
                if (start_inx in range(start_inx_Gold, end_inx_Gold+1)  or end_inx in range(start_inx_Gold, end_inx_Gold+1) ):
                    
                    if (tag_part_Gold['phrase'] == tag_part['phrase'] and tag_part_Gold['phrase'].strip() !=''):
                        tp +=1
                        Gold.remove(tag_part_Gold)
                        annotator.remove(tag_part)
                        break
            
            else:
                if (tag_part_Gold['phrase'] == tag_part['phrase'] and tag_part_Gold['phrase'].strip() !=''):
                        tp +=1
                        Gold.remove(tag_part_Gold)
                        annotator.remove(tag_part)
                        break
                    
    fp = len(Gold)
    fn = len(annotator)
    Recall = float(tp) / (tp + fn)
    Precision = float(tp) / (tp + fp)
    f_score = (2 * Recall * Precision) / (Recall + Precision)
    
    
    return [Precision, Recall, f_score]#, [tp, fn, fp]
    

def EntityPartialMatching(tag, goldJson, annotatorJson, threshold):
    
    '''
    doing the partial match
    '''
    tp , fp , fn = 0, 0, 0
    
    tag_parts_Gold = json.loads(goldJson)[tag]
    tag_parts = json.loads(annotatorJson)[tag]
    
    Gold = list()
    annotator = list()
    
    for g in tag_parts_Gold:
        if g not in Gold:
            Gold.append(g)
    
    for g in tag_parts:
        if g not in annotator:
            annotator.append(g)
    
    
    for tag_part in tag_parts: 
        
        if (tag_part in Gold):
            tp +=1
            Gold.remove(tag_part)
            annotator.remove(tag_part)
            tag_parts_Gold.remove(tag_part)
#            print tag_part
            continue
            
    tag_parts = list()
    for g in annotator:
        if g not in tag_parts:
            tag_parts.append(g)
    
    for tag_part_Gold in tag_parts_Gold:
        for tag_part in tag_parts: 
            
            if ( tag_part not in annotator or tag_part_Gold not in Gold):
                continue
            
            if (';' not in tag_part_Gold['inx'] and ';' not in tag_part['inx']):
                [start_inx_Gold, end_inx_Gold] = [int(i) for i in tag_part_Gold['inx'].split() ]
                [start_inx, end_inx] = [int(i) for i in tag_part['inx'].split() ]
                
                if (start_inx in range(start_inx_Gold, end_inx_Gold+1)  or end_inx in range(start_inx_Gold, end_inx_Gold +1) \
                    or start_inx_Gold in range(start_inx, end_inx+1)  or end_inx_Gold in range(start_inx, end_inx +1) ):
                    
                    if  fuzz.ratio(tag_part_Gold['phrase'], tag_part['phrase']) > threshold:
                        tp +=1
                        Gold.remove(tag_part_Gold)
                        annotator.remove(tag_part)
                        tag_parts.remove(tag_part)
#                        print tag_part_Gold
#                        print tag_part
                        break
            
            else:
                if fuzz.ratio(tag_part_Gold['phrase'] , tag_part['phrase']) > threshold:
                    Gold.remove(tag_part_Gold)
                    annotator.remove(tag_part)
                    tag_parts.remove(tag_part)
                    tp +=1
#                    print tag_part_Gold
#                    print tag_part
                    break
                    
    fp = len(Gold)
    fn = len(annotator)
    Recall = float(tp) / (tp + fn)
    Precision = float(tp) / (tp + fp)
    f_score = (2 * Recall * Precision) / (Recall + Precision)
    
    
    return [Precision, Recall, f_score]#, [tp, fn, fp]


def RelationExactMatching(tag, goldJson, annotatorJson):
    
    '''
    doing the exact match
    '''
    tp , fp , fn = 0, 0, 0
    
    tag_parts_Gold = json.loads(goldJson)[tag]
    tag_parts = json.loads(annotatorJson)[tag]
    
    Gold = list()
    annotator = list()
    
    for g in tag_parts_Gold:
        if g not in Gold:
            Gold.append(g)
    
    for g in tag_parts:
        if g not in annotator:
            annotator.append(g)
    
    for tag_part_Gold in tag_parts_Gold:
        for tag_part in tag_parts: 
            
            if ( tag_part not in annotator or tag_part_Gold not in Gold):
                continue
            
            if (tag_part_Gold['Arg1'][2] == tag_part['Arg1'][2] and tag_part_Gold['Arg2'][2] == tag_part['Arg2'][2] and tag_part_Gold['Arg1'][2] !='' and tag_part_Gold['Arg2'][2]!=''):
                tp +=1
                Gold.remove(tag_part_Gold)
                annotator.remove(tag_part)
                break
                    
    fp = len(Gold)
    fn = len(annotator)
    Recall = float(tp) / (tp + fn)
    Precision = float(tp) / (tp + fp)
    f_score = (2 * Recall * Precision) / (Recall + Precision)
    
    
    return [Precision, Recall, f_score]#, [tp, fn, fp]


def RelationPartialMatching(tag, goldJson, annotatorJson, threshold):
    
    '''
    doing the exact match
    '''
    tp , fp , fn = 0, 0, 0
    
    tag_parts_Gold = json.loads(goldJson)[tag]
    tag_parts = json.loads(annotatorJson)[tag]
    
    Gold = list()
    annotator = list()
    
    for g in tag_parts_Gold:
        if g not in Gold:
            Gold.append(g)
    
    for g in tag_parts:
        if g not in annotator:
            annotator.append(g)
    
    
    for tag_part in tag_parts: 
        
        if (tag_part in Gold):
            tp +=1
            Gold.remove(tag_part)
            annotator.remove(tag_part)
            tag_parts_Gold.remove(tag_part)
            #print tag_part
            continue
            
    tag_parts = list()
    for g in annotator:
        if g not in tag_parts:
            tag_parts.append(g)
    
    for tag_part_Gold in tag_parts_Gold:
        for tag_part in tag_parts: 
            
            if ( tag_part not in annotator or tag_part_Gold not in Gold):
                continue
                      
            if ( fuzz.ratio(tag_part_Gold['Arg1'][2], tag_part['Arg1'][2]) > threshold and fuzz.ratio(tag_part_Gold['Arg2'][2], tag_part['Arg2'][2]) >threshold ):
                tp +=1
                Gold.remove(tag_part_Gold)
                annotator.remove(tag_part)
                tag_parts.remove(tag_part)
                break
                    
    fp = len(Gold)
    fn = len(annotator)
    Recall = float(tp) / (tp + fn)
    Precision = float(tp) / (tp + fp)
    f_score = (2 * Recall * Precision) / (Recall + Precision)
    
    
    return [Precision, Recall, f_score]


#goldJson = Ann2Json('./Unchanges/protest_JJ/protest_round_4/AFP_SPA_20000412.0410.ann')
#annotatorJson = Ann2Json('./Unchanges/protest_JJ/protest_round_5/AFP_SPA_20000412.0410.ann')
#
#result = EntityExactMatching('source', goldJson, annotatorJson)
#
#print result