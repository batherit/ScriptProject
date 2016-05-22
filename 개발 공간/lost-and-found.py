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

#xmlFD = -1
kindOfGoodsXMLDoc = None

lostsDoc = None
foundsDoc = None

informOfFoundsXMLDoc = None
informOfLostsXMLDoc = None

serviceKey = "&ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D"


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
        #PrintDetailOfLosts()
        if kindOfGoodsXMLDoc != None:
            kindOfFounds = SelectKindOfGoods()
            startDay, endDay = InsertSearchPeriod()
            PrintInformOfFounds(kindOfFounds, startDay, endDay)
        else : print("※해당 데이터가 존재하지 않습니다.※")
    elif menu == 'l':
        #PrintDetailOfLosts()
        if kindOfGoodsXMLDoc  != None:
            kindOfLosts = SelectKindOfGoods()
            startDay, endDay = InsertSearchPeriod()
            PrintInformOfLosts(kindOfLosts, startDay, endDay)
        else : print("※해당 데이터가 존재하지 않습니다.※")
    elif menu == 'q':
        QuitLAF()
    else:
        print ("※잘못된 키 입력입니다.※")
        
        
#### xml function implementation
def LoadXMLFromWeb():
    global kindOfGoodsXMLDoc 

    try:
        xmlFD = urlopen("http://openapi.lost112.go.kr/openapi/service/rest/CmmnCdService/getThngClCd?ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D")
    except IOError:
        print ("※URL 접근에 실패하였습니다.※")
        
        return False
    else:
        try:
            kindOfGoodsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("※읽어오기가 실패하였습니다.※")
        else:
            print ("성공적으로 xml 파일을 읽어왔습니다.")
            return True
    return False
    
    
def LAFFree():
    global kindOfGoodsXMLDoc 
    global informOfFoundsXMLDoc
    global informOfLostsXMLDoc
    
    if checkKOGDoc(): kindOfGoodsXMLDoc .unlink()   # minidom 객체 해제합니다.
    if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
    if checkIOLDoc(): informOfLostsXMLDoc.unlink()
     
def QuitLAF():
    global loopFlag
    loopFlag = 0
    LAFFree()
         
           
def SelectKindOfGoods():
    global kindOfGoodsXMLDoc
    #kind_losts_dic = {  "prdtCd" : "물품 분류 코드 :", "prdtNm" : "물품 분류명 :" }
    if not checkKOGDoc():  # DOM이 None인지 검사합니다.
        return None
        
    response = kindOfGoodsXMLDoc.childNodes
    rsp_child = response[0].childNodes
    
    for item in rsp_child:
        if item.nodeName == "body":                 
            body_list = item.childNodes             
            items = body_list[0]                    
            items_list = items.childNodes
            for i, item in enumerate(items_list):
                item_list = item.childNodes
                if 0 == i % 3 :
                    print('')
                print("{0:<2}. {1:<10}".format(i, item_list[1].firstChild.nodeValue), end = ' ')
                
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
        if 8 == len(startDay) and int(startDay[2]+startDay[3]) >=14 \
           and 1<=int(startDay[4]+startDay[5]) <= 12 and 1<=int(startDay[6]+startDay[7]) <= 31 :
            break
        else : print("※잘못된 입력입니다.※")
    
    while 1:
        endDay = input("검색 시작일 이후, 검색 종료일을 입력해주세요.:")
        if 8 == len(endDay) and (int(startDay) <= int(endDay)) \
           and 1<=int(endDay[4]+endDay[5]) <= 12 and 1<=int(endDay[6]+endDay[7]) <= 31:
            break 
        else : print("※잘못된 입력입니다.※")      
    
    return startDay, endDay
    

def PrintInformOfFounds(kindOfFounds, startDay, endDay):
    global serviceKey
    global informOfFoundsXMLDoc
    pageNum = 1
    
    founds_inform_dic = \
    { 
        "atcId" : "관리 ID :", "fdSn" : "습득 순번 :","prdtClNm" : "물품 분류명 :",
         "clrNm" : "색상명 :","fdPrdtNm" : "물품명 :", "fdSbjt" : "게시 제목 :",
        "fdFilePathImg" : "이미지 경로 :", "depPlace" : "관리 장소 :", "fdYmd" : "습득 날짜 :"
    }
    
    while 1:
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+kindOfFounds+"&START_YMD="+startDay+"&END_YMD="+endDay+"&pageNo="+str(pageNum)
        totalURL = basedURL+optionURL+serviceKey
        #print(totalURL)
        try:
            xmlFD = urlopen(totalURL)
        except IOError:
            print ("※URL 접근에 실패하였습니다.※")
        else:
            try:
                informOfFoundsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
            except Exception:
                print ("※읽어오기가 실패하였습니다.※")
            else:
                print ("검색 조건에 해당하는 정보들을 출력합니다.")
                response = informOfFoundsXMLDoc.childNodes
                rsp_child = response[0].childNodes
                for item in rsp_child:
                    if item.nodeName == "body":                 
                        body_list = item.childNodes             
                        items = body_list[0]                    
                        items_list = items.childNodes
                        if 0 != len(items_list):
                            for i, item in enumerate(items_list):
                                print("---------<<{0}>>---------".format(i))
                                item_list = item.childNodes
                                for founds_inform in item_list:
                                    if founds_inform.nodeName != "rnum":
                                        print(founds_inform_dic[founds_inform.nodeName], founds_inform.firstChild.nodeValue)
                        else : 
                            print("※나타낼 데이터가 없습니다.※")
                print("                              -{0}-".format(pageNum))
        while 1:
            key = input("이전 장 : [, 이후 장 : ], 종료 : q를 입력하세요. :")
            if key != '[' and key != ']' and key != 'q': 
                print("※잘못된 입력입니다.※")
            elif key == '[':
                if pageNum > 1 :
                    pageNum = pageNum-1
                    break
                else :
                    print("※더 이상 표시할 수 없는 페이지입니다.※")
                    break
            elif key == ']':
                pageNum = pageNum + 1
                break
            else : return None
            
def PrintInformOfLosts(kindOfLosts, startDay, endDay):
    global serviceKey
    global informOfLostsXMLDoc
    pageNum = 1
    
    losts_inform_dic = \
    { 
        "atcId" : "관리 ID :","lstPlace" : "분실 지역명 :", "prdtClNm" : "물품 분류명 :",
        "lstPrdtNm" : "분실물명 :", "lstSbjt" : "게시 제목 :", "lstYmd": "분실물 등록 날짜 :"
    }
    
    while 1:
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+kindOfLosts+"&START_YMD="+startDay+"&END_YMD="+endDay+"&pageNo="+str(pageNum)
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
                        if 0 != len(items_list):
                            for i, item in enumerate(items_list):
                                print("---------<<{0}>>---------".format(i))
                                item_list = item.childNodes
                                for losts_inform in item_list:
                                    if losts_inform.nodeName != "rnum":
                                        print(losts_inform_dic[losts_inform.nodeName], losts_inform.firstChild.nodeValue)
                        else : 
                            print("※나타낼 데이터가 없습니다.※")
                print("                              -{0}-".format(pageNum))
        while 1:
            key = input("이전 장 : [, 이후 장 : ], 종료 : q를 입력하세요. :")
            if key != '[' and key != ']' and key != 'q': 
                print("※잘못된 입력입니다.※")
            elif key == '[':
                if pageNum > 1 :
                    pageNum = pageNum-1
                    break
                else :
                    print("※더 이상 표시할 수 없는 페이지입니다.※")
                    break
            elif key == ']':
                pageNum = pageNum + 1
                break
            else : return None

def checkKOGDoc():
    global kindOfGoodsXMLDoc 
    if kindOfGoodsXMLDoc  == None:
        print("※읽어올 xml 파일이 존재하지 않습니다.※")
        return False
    return True

def checkIOFDoc():
    global informOfFoundsXMLDoc 
    if informOfFoundsXMLDoc  == None:
        print("※읽어올 xml 파일이 존재하지 않습니다.※")
        return False
    return True

def checkIOLDoc():
    global informOfLostsXMLDoc 
    if informOfLostsXMLDoc  == None:
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
    
