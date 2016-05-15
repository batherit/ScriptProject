# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:14:00 2016

@author: 심정환PC
"""

from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree
from urllib.request import urlopen

##### global
loopFlag = 1
xmlFD = -1
LostsDoc = None

kindOfLostsXMLDoc = None
informOfLostsXMLDoc = None

serviceKey = "&ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D"


#### Menu  implementation
def printMenu():
    print("========<<메뉴>>==========")
    print("xml 파일을 읽어옵니다.: l")
    print("상세정보를 출력합니다.: b")
    print("프로그램을 종료합니다.: q")
    print("==================")
    
    
def launcherFunction(menu):
    global LostsDoc
    if menu ==  'l':
        LoadXMLFromWeb()
    elif menu == 'b':
        #PrintDetailOfLosts()
        if kindOfLostsXMLDoc  != None:
            kindOfLosts = SelectKindOfLosts()
            startDay, endDay = InsertSearchPeriod()
            PrintInformOfLosts(kindOfLosts, startDay, endDay)
        else : print("※해당 데이터가 존재하지 않습니다.※")
    elif menu == 'q':
        QuitLAF()
    else:
        print ("※잘못된 키 입력입니다.※")
        
        
#### xml function implementation
def LoadXMLFromWeb():
    global kindOfLostsXMLDoc

    try:
        xmlFD = urlopen("http://openapi.lost112.go.kr/openapi/service/rest/CmmnCdService/getThngClCd?ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D")
    except IOError:
        print ("※URL 접근에 실패하였습니다.※")
        
        return False
    else:
        try:
            kindOfLostsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("※읽어오기가 실패하였습니다.※")
        else:
            print ("성공적으로 xml 파일을 읽어왔습니다.")
            return True
    return False
    
    
def LAFFree():
    global kindOfLostsXMLDoc 
    global informOfLostsXMLDoc
    
    if checkDocument():
        kindOfLostsXMLDoc.unlink()   # minidom 객체 해제합니다.
        informOfLostsXMLDoc.unlink()
     
     
def QuitLAF():
    global loopFlag
    loopFlag = 0
    LAFFree()
         
           
def SelectKindOfLosts():
    global kindOfLostsXMLDoc
    #kind_losts_dic = {  "prdtCd" : "물품 분류 코드 :", "prdtNm" : "물품 분류명 :" }
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None
        
    response = kindOfLostsXMLDoc.childNodes
    rsp_child = response[0].childNodes
    
    for item in rsp_child:
        if item.nodeName == "body":                 
            body_list = item.childNodes             
            items = body_list[0]                    
            items_list = items.childNodes
            for i, item in enumerate(items_list):
                item_list = item.childNodes
                print("{0}. {1}".format(i, item_list[1].firstChild.nodeValue))
                
    while 1:        
        kindIdx=int(input("위 목록 중 찾을 물품 종류를 골라주세요.^^:"))
        if 0 <= kindIdx <= 18:
            item = items_list[kindIdx]
            item_list = item.childNodes
            print("'{0}'을(를) 선택하셨습니다.".format(item_list[1].firstChild.nodeValue))
            return item_list[0].firstChild.nodeValue
        else: print("※잘못된 입력입니다.※")
        
        
def InsertSearchPeriod():
    while 1:
        startDay = input("2014년 1월 이후, 검색 시작일을 입력해주세요.:")
        if 8 != len(startDay) or (int(startDay[2]) <= 1 and int(startDay[3]) <= 3):
            print("※잘못된 입력입니다.※")
        else : break
    
    while 1:
        endDay = input("검색 시작일 이후, 검색 종료일을 입력해주세요.:")
        if 8 != len(endDay) or (int(startDay) > int(endDay)):
            print("※잘못된 입력입니다.※")
        else : break       
    
    return startDay, endDay
    

def PrintInformOfLosts(kindOfLosts, startDay, endDay):
    global serviceKey
    global informOfLostsXMLDoc
    losts_inform_dic = \
    { 
        "atcId" : "관리 ID :", "fdSn" : "습득 순번 :","prdtClNm" : "물품 분류명 :",
         "clrNm" : "색상명 :","fdPrdtNm" : "물품명 :", "fdSbjt" : "게시 제목 :",
        "fdFilePathImg" : "이미지 경로 :", "depPlace" : "관리 장소 :", "fdYmd" : "습득 날짜 :"
    }
    basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?"
    optionURL = "PRDT_CL_CD_01="+kindOfLosts+"&START_YMD="+startDay+"&END_YMD="+endDay
    totalURL = basedURL+optionURL+serviceKey
    #print(totalURL)
    try:
        xmlFD = urlopen(totalURL)
    except IOError:
        print ("※URL 접근에 실패하였습니다.※")
    else:
        try:
            informOfLostsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("※읽어오기가 실패하였습니다.※")
        else:
            print ("검색 조건에 해당하는 정보들을 출력합니다.")
            response = informOfLostsXMLDoc.childNodes
            rsp_child = response[0].childNodes
            for item in rsp_child:
                if item.nodeName == "body":                 
                    body_list = item.childNodes             
                    items = body_list[0]                    
                    items_list = items.childNodes
                    for i, item in enumerate(items_list):
                        print("---------<<{0}>>---------".format(i))
                        item_list = item.childNodes
                        for losts_inform in item_list:
                            if losts_inform.nodeName != "rnum":
                                print(losts_inform_dic[losts_inform.nodeName], losts_inform.firstChild.nodeValue)


def checkDocument():
    global kindOfLostsXMLDoc 
    if kindOfLostsXMLDoc  == None:
        print("※읽어올 xml 파일이 존재하지 않습니다.※")
        return False
    return True


##### run #####
print("안녕하세요. '분실물 찾아요' 서비스입니다.")
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('메뉴를 선택해주세요.^^ :'))
    launcherFunction(menuKey)
else:
    print ("감사합니다. 좋은 하루되세요~^^")
    
