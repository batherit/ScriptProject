# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:41:05 2016

@author: 심정환PC
"""

import spam

def sort_list(goodsList):
    nItem  = len(goodsList)
    for i in range(nItem - 1):
        for j in range(nItem - 1 - i):
            ymd1 = spam.atol(goodsList[j][1].replace('-',''))
            ymd2 = spam.atol(goodsList[j+1][1].replace('-', ''))
            if ymd1 < ymd2:
                goodsList[j], goodsList[j+1] = goodsList[j+1], goodsList[j]
    
