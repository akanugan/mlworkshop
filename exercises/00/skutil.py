#!/usr/bin/env python
#------------------------------------------------------------------------------
# File: skutil.py
# Description: some sklearn utilities
# Created: 03-Mar-2018 Harrison B. Prosper
#------------------------------------------------------------------------------
import os, sys
import numpy as np
from string import *
#------------------------------------------------------------------------------
def bootstrap_unweight(df, weightname='weight'):
    from math import sqrt
    from random import uniform
    
    def binsearch(L, item):
        first = 0
        last  = len(L) - 1   
        found = False
        while (first <= last) and not found:
            mid = (first + last) / 2
            if item <= L[mid]:
                last = mid;       
            elif item > L[mid]:
                first = mid + 1
            if first >= last:
                mid = first
                found = True
        if found: return mid
        return -1

    w1 = df[weightname]
    w2 = w1*w1
    w1sum = sum(w1)
    w2sum = sum(w2)
    count = int(w1sum*w1sum / w2sum)
    wcdf  = np.cumsum(w1)
    print "summed weight sum: %10.4f" % w1sum
        
    wlist = wcdf.tolist()
    index = []
    for i in xrange(count):
        w = uniform(0, w1sum)
        k = binsearch(wlist, w)
        if k < 0 or k > len(wlist)-1:
            print "**error** location of weight %f not found" % w
            return None
        index.append(k)
    return df.iloc[index]
