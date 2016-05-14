# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:14:00 2016

@author: 심정환PC
"""
from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree

##### global
loopFlag = 1
xmlFD = -1
LostsDoc = None

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
        LostsDoc = LoadXMLFromFile()
    elif menu == 'b':
        PrintDetailOfLosts()
    elif menu == 'q':
        QuitLAF()
    else:
        print ("error : unknow menu key")
        
#### xml function implementation
def LoadXMLFromFile():
   # fileName = str(input ("읽어올 xml 파일명을 입력하세요. :"))  # open 메소드 사용 시 에러!
    global xmlFD
 
    try:
        xmlFD = "te.xml"#open(fileName)   # xml 문서를 open합니다.
    except IOError:
        print ("※유효하지 않은 파일명 또는 경로입니다.※")
        return None
    else:
        try:
            dom = parse(xmlFD)   # XML 문서를 파싱합니다.
        except Exception:
            print ("※읽어오기가 실패하였습니다.※")
        else:
            print ("성공적으로 xml 파일을 읽어왔습니다.")
            return dom
    return None
    
def LAFFree():
    global LostsDoc 
    if checkDocument():
        LostsDoc.unlink()   # minidom 객체 해제합니다.
     
def QuitLAF():
    global loopFlag
    loopFlag = 0
    LAFFree()
    
def PrintDetailOfLosts():
    global LostsDoc
    detail_inform_dic = \
    { 
        "atcId" : "관리 ID :", "csteSteNm" : "보관 상태 :", "depPlace" : "관리 장소 :",
        "fdFilePathImg" : "이미지 경로 :", "fdHor" : "습득 시간 :", "fdPlace" : "습득 장소 :",
        "fdPrdtNm" : "물품명 :", "fdSn" : "습득 순번 :", "fdYmd" : "습득 날짜 :", 
        "fndKeepOrgnSeNm" : "습득물 보관 기관 구분명 :", "orgId" : "기관 ID :",
        "orgNm" : "기관명 :", "prdtClNm" : "물품 분류명 :", "tel" : "전화 번호 :",
        "uniq" : "특이 사항 :"
    }
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None
    
    response = LostsDoc.childNodes
    rsp_child = response[0].childNodes
    for item in rsp_child:
        if item.nodeName == "body":                 # response 자식 중 body를 골라낸다.
            body_list = item.childNodes             # body의 자식 리스트를 추출한다.
            for item in body_list:                  # item을 찾는다.
                item_list = item.childNodes         # item의 자식 리스트를 추출한다.
                for detail_inform in item_list:
                    print(detail_inform_dic[detail_inform.nodeName], detail_inform.firstChild.nodeValue)
def checkDocument():
    global LostsDoc
    if LostsDoc == None:
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
    print ("Thank you! Good Bye")