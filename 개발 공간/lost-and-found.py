# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:14:00 2016

@author: 심정환PC
"""

from search import *

##### global
loopFlag = 1

#### Menu  implementation
def printMenu():
    print("========<<메뉴>>==========")
    print("xml 파일을 읽어옵니다.: r")
    print("습득물 검색 : f")
    print("분실물 검색 : l")
    print("프로그램을 종료합니다.: q")
    print("==================")

def launcherFunction(menu):
    global LostsDoc
    if menu ==  'r':
        LoadXMLFromWeb()
    elif menu == 'f':
        if checkKOGDoc() :
            while 1:    
                print("주소별 검색 : a, 종류별 검색 : k")
                key = input("원하는 메뉴를 입력하세요. :")
                if key == 'a':
                    addr = InputAddr()
                    founds = WhatLostIt()
                    PrintInformOfFoundsByAddr(addr, founds)
                    break
                elif key == 'k':
                    kindOfFounds = SelectKindOfGoods()
                    startDay, endDay = InsertSearchPeriod()
                    PrintInformOfFoundsByKind(kindOfFounds, startDay, endDay)
                    break
                else:
                    print("※잘못된 키 입력입니다.※")
        else : print("※해당 데이터가 존재하지 않습니다.※")
    elif menu == 'l':
        if checkKOGDoc() :
            while 1:    
                print("장소별 검색 : l, 종류별 검색 : k")
                key = input("원하는 메뉴를 입력하세요. :")
                if key == 'l':
                    location = WhereLoseIt()
                    losts = WhatLostIt()
                    PrintInformOfLostsByLocation(location, losts)
                    break
                elif key == 'k':
                    kindOfLosts = SelectKindOfGoods()
                    startDay, endDay = InsertSearchPeriod()
                    PrintInformOfLostsByKind(kindOfLosts, startDay, endDay)
                    break
                else:
                    print ("※잘못된 키 입력입니다.※")
            
        else : print("※해당 데이터가 존재하지 않습니다.※")
    elif menu == 'q':
        QuitLAF()
    else:
        print ("※잘못된 키 입력입니다.※")

def QuitLAF():
    global loopFlag
    loopFlag = 0
    LAFFree()


##### run #####
print("안녕하세요. '분실물 찾아요' 서비스입니다.")
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('메뉴를 선택해주세요.^^ :'))
    launcherFunction(menuKey)
else:
    print ("감사합니다. 좋은 하루되세요~^^")
    
