from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree
from urllib.request import urlopen, quote
#from gmail import *
from os import system


from gmailGUI import MyTransmitEmailMenuForm
from PyQt4 import QtGui, QtCore

import founds_menu_ui
import losts_menu_ui
import founds_addr_search_menu_ui
import founds_kind_search_menu_ui
import founds_detail_menu_ui

kindOfGoodsXMLDoc = None

lostsDoc = None
foundsDoc = None

informOfFoundsXMLDoc = None
informOfLostsXMLDoc = None

foundsDetailBasket = []
lostsDetailBasket = []

serviceKey = "&ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D"

class MyFoundsMenuForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = founds_menu_ui.Ui_Form()
        self.ui.setupUi(self)

    def menu_founds_addr(self):
        self.addrSearch = MyFoundsAddrSearchForm()
        self.addrSearch.show()
        self.close()
        return
    
    def menu_founds_kind(self):
        self.kindSearch = MyFoundsKindSearchForm()
        self.kindSearch.show()
        self.close()
        return

class MyLostsMenuForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = losts_menu_ui.Ui_Form()
        self.ui.setupUi(self)

    def menu_losts_location(self):
        return
    
    def menu_losts_kind(self):
        return
        
class MyFoundsDetailMenuForm(QtGui.QMainWindow):
    goodsDetailList = []
    def __init__(self, parent=None, row=0, col=0):
        global informOfFoundsXMLDoc
        #global row, col
        QtGui.QWidget.__init__(self, parent)

        self.ui = founds_detail_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        founds_detail_dic = \
        { 
            0: "fdPrdtNm" , 1 : "fdYmd", 2 : "fdHor",
            3: "fdPlace"  , 4 : "atcId", 5 : "csteSteNm",
            6: "depPlace" , 7 : "tel"  , 8 : "uniq"
        }
        
        try:
            tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml())) #ElementTree                       
            items = tree.getiterator("item")  
            for i, item in enumerate(items):
                if i == int(row):
                    detailURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundDetailInfo?"+"ATC_ID="+item.find("atcId").text +"&FD_SN="+item.find("fdSn").text+serviceKey                       
            try:
                xmlFD = urlopen(detailURL)
            except IOError:
                print ("※URL 접근에 실패하였습니다.※")
            else:
                try:
                    detailOfFoundsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
                except Exception:
                    print ("※읽어오기가 실패하였습니다.※")
                else:
                    #goodsDetailList = []
                    print ("세부 정보를 출력합니다.")
                    tree = ElementTree.fromstring(str(detailOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")    
                    for item in items:
                        for i in range(9):
                            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find(founds_detail_dic[i]).text))
                            self.goodsDetailList.append((founds_detail_dic[i],item.find(founds_detail_dic[i]).text))
                            
        except Exception:
            print ("※트리 파싱에 에러가 발생하였습니다.※")
        return

    def click_close(self):
        self.close()
        return
        
    def transmit_email(self):
        self.transmitEmailMenu = MyTransmitEmailMenuForm(None, self.goodsDetailList, "습득물")
        self.transmitEmailMenu.show()
        self.goodsDetailList.clear()
        return
        
    def put_on_list(self):
        return
        
    def transmit_email_list(self):
        return

class MyFoundsAddrSearchForm(QtGui.QMainWindow):
    pageNum = 1
    addr = None
    founds = None
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = founds_addr_search_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
    def founds_addr_search(self):
        global serviceKey
        global informOfFoundsXMLDoc
        
        self.addr = self.ui.lineEdit.text()
        self.founds = self.ui.lineEdit_2.text()     
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToLc?"
        optionURL = "PRDT_NM="+quote(self.founds)+"&ADDR="+quote(self.addr)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def founds_print_detail(self, row, col):
        if not bool(self.ui.tableWidget.item(row, col)): return
        self.foundsDetailMenu = MyFoundsDetailMenuForm(None, row, col)
        self.foundsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfFoundsXMLDoc
        
        if not checkIOFDoc(): return
        self.pageNum += 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToLc?"
        optionURL = "PRDT_NM="+quote(self.founds)+"&ADDR="+quote(self.addr)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfFoundsXMLDoc
        
        if not checkIOFDoc(): return
        if self.pageNum == 1 : return        
        self.pageNum -= 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToLc?"
        optionURL = "PRDT_NM="+quote(self.founds)+"&ADDR="+quote(self.addr)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_back(self):
        global informOfFoundsXMLDoc
        
        self.founds = None
        self.addr = None
        self.pageNum = 1
        self.nItems = 0
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return
        
class MyFoundsKindSearchForm(QtGui.QMainWindow):
    pageNum = 1
    kind = None
    startDay = None
    endDay = None
    items_list = None
    
    def __init__(self, parent=None):
        global kindOfGoodsXMLDoc
        QtGui.QWidget.__init__(self, parent)
        self.ui = founds_kind_search_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.response = kindOfGoodsXMLDoc.childNodes
        self.rsp_child = self.response[0].childNodes
        self.body_list = self.rsp_child[1].childNodes
        self.items = self.body_list[0]
        self.items_list = self.items.childNodes
        
    def founds_kind_search(self):
        global serviceKey
        global informOfFoundsXMLDoc
        
        self.kind = (self.items_list[self.ui.comboBox.currentIndex()].childNodes)[0].firstChild.nodeValue
        self.startDay = self.ui.lineEdit.text()
        self.endDay = self.ui.lineEdit_2.text()
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def founds_print_detail(self, row, col):
        if not bool(self.ui.tableWidget.item(row, col)): return
        self.foundsDetailMenu = MyFoundsDetailMenuForm(None, row, col)
        self.foundsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfFoundsXMLDoc
        
        if not checkIOFDoc(): return
        self.pageNum += 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfFoundsXMLDoc
        
        if not checkIOFDoc(): return
        if self.pageNum == 1 : return        
        self.pageNum -= 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i, item in enumerate(items):
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_back(self):
        global informOfFoundsXMLDoc
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        self.nItems = 0
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return

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
    
def LAFFree():
    global kindOfGoodsXMLDoc 
    global informOfFoundsXMLDoc
    global informOfLostsXMLDoc

    if checkKOGDoc(): kindOfGoodsXMLDoc .unlink()   # minidom 객체 해제합니다.
    if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
    if checkIOLDoc(): informOfLostsXMLDoc.unlink()
