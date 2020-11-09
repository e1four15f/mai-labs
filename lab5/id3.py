#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import sys
import math
from collections import Counter
from anytree import Node, RenderTree
from anytree.exporter import DotExporter



def entropy(df, target):
    
    entropy = 0.
    n = len(df)
    
    P = Counter(df[target])
    
    for label in P.keys():
        p_i = P[label] / n
        entropy -= p_i * math.log(p_i, 2)
        
    return entropy



def IG(feature, df, target): 
    
    IG = entropy(df, target)
    
    P = Counter(df[feature])
    n = len(df)
    
    for label in P.keys():
        IG -= (P[label] / n) * entropy(df[df[feature]==label], target)
    
    return IG



def ID3(df, target, features_to_explore, connect_node=None, i=0):

    if df.empty:
        return
    elif (not features_to_explore) & (df[target].nunique() == 1):
        Node(f'{i + 1}. class: {df[target][0]}', parent=connect_node)
        return
    elif (not features_to_explore):
        Node(f'{i + 1}. classes: {df[target].unique()}', parent=connect_node)
        return
    elif df[target].nunique() == 1:
        Node(f'{i + 1}. class: {df[target][0]}', parent=connect_node)
        return
    
    features_IG = {}
    for feature in features_to_explore:
        features_IG[feature] = IG(feature, df, target)
    
    best_node = max(features_IG, key=features_IG.get)
    i+=1
    best = Node(f'{i}. {best_node} IG={round(features_IG[best_node],4)}', parent=connect_node)
    
    remaining_features = [feature for feature in features_to_explore if feature != best_node]

    i+=1
    for label, subset in df.groupby(best_node):
        connect_node = Node(f'{i}. {label} Entropy={round(entropy(subset, target),4)}', 
                            parent=best)
        
        subtree = ID3(subset,
                      target,
                      remaining_features,
                      connect_node, 
                      i=i)
        
    DotExporter(best).to_picture("data/decision_tree.png")
    
    return 


if __name__ == '__main__':

    df = pd.read_csv('data/group.csv').set_index('ФИО')

    target = str(sys.argv)

    features_to_explore = [feature for feature in df if feature != target]

    decision_tree = ID3(df, target, features_to_explore)


