from xml.dom.minidom import parse, parseString # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree
from urllib.request import urlopen, quote
#from gmail import *
from os import system


from gmailGUI import MyTransmitEmailMenuForm, RunPreviewServer
from PyQt4 import QtGui, QtCore

import main_menu_ui

import law_menu_ui
import founds_menu_ui
import losts_menu_ui

import founds_addr_search_menu_ui
import founds_kind_search_menu_ui
import founds_detail_menu_ui

import losts_location_search_menu_ui
import losts_kind_search_menu_ui
import losts_detail_menu_ui

from sortGUI import sort_list

import webbrowser

kindOfGoodsXMLDoc = None

lostsDoc = None
foundsDoc = None

informOfFoundsXMLDoc = None
informOfLostsXMLDoc = None

foundsDetailBasket = []
lostsDetailBasket = []
item_list = []

serviceKey = "&ServiceKey=jbfaPFGDu0gyILL0E6rWgZe1Fq1Y60tCFkC3ErTPctXTPWgs8AqAxetBbec7tYOJIRWHGZ9N77NLdVuWBR6nlg%3D%3D"
chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

class MyMainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        global kindOfGoodsXMLDoc
        if checkKOGDoc(): 
            kindOfGoodsXMLDoc .unlink()
            kindOfGoodsXMLDoc = None
            
        LoadXMLFromWeb()

        self.ui = main_menu_ui.Ui_Form()
        self.ui.setupUi(self)

    def menu_founds(self):
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return

    def menu_losts(self):
        self.lostsMenu = MyLostsMenuForm()
        self.lostsMenu.show()
        self.close()
        return
        
    def click_law(self):
        self.lawMenu = MyLawMenuForm()
        self.lawMenu.show()
        return
        
class MyLawMenuForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = law_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
    def click_close(self):
        self.close()
        return

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
        self.locationSearch = MyLostsLocationSearchForm()
        self.locationSearch.show()
        self.close()
        return
    
    def menu_losts_kind(self):
        self.kindSearch = MyLostsKindSearchForm()
        self.kindSearch.show()
        self.close()
        return
        
class MyFoundsDetailMenuForm(QtGui.QMainWindow):
    goodsDetailList = []
    detailOfFoundsXMLDoc = None
    def __init__(self, parent=None, row=0, col=0):
        global informOfFoundsXMLDoc
        global foundsDetailBasket
        global lostDetailBasket
        global item_list
        
        #global row, col
        QtGui.QWidget.__init__(self, parent)

        self.ui = founds_detail_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])
        
        founds_detail_dic_idx = \
        { 
            0: "fdPrdtNm" , 1 : "fdYmd", 2 : "fdHor",
            3: "fdPlace"  , 4 : "atcId", 5 : "csteSteNm",
            6: "depPlace" , 7 : "tel"  , 8 : "uniq"
        }
        founds_detail_dic_str = \
        { 
            "fdPrdtNm" : "물품명 :", "fdYmd" : "습득 일자 :" , "fdHor" : "습득 시간 :", 
            "fdPlace" : "습득 장소 :", "atcId" : "관리 ID :" , "csteSteNm" : "보관 상태 :",
            "depPlace" : "보관 장소 :", "tel" : "전화번호 :", "uniq" : "특이사항 :"
        }
        
        
        try:
            tree = ElementTree.fromstring(str(informOfFoundsXMLDoc.toxml())) #ElementTree                       
            items = tree.getiterator("item")  
            for i, item in enumerate(items):
                if i == int(row):
                    #detailURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundDetailInfo?"+"ATC_ID="+item.find("atcId").text +"&FD_SN="+item.find("fdSn").text+serviceKey 
                    detailURL = "http://openapi.lost112.go.kr/openapi/service/rest/LosfundInfoInqireService/getLosfundDetailInfo?"+"ATC_ID="+item_list[i][4] +"&FD_SN="+item_list[i][5]+serviceKey                      
            try:
                xmlFD = urlopen(detailURL)
            except IOError:
                print ("※URL 접근에 실패하였습니다.※")
            else:
                try:
                    self.detailOfFoundsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
                except Exception:
                    print ("※읽어오기가 실패하였습니다.※")
                else:
                    #goodsDetailList = []
                    print ("세부 정보를 출력합니다.")
                    tree = ElementTree.fromstring(str(self.detailOfFoundsXMLDoc.toxml()))
                    items = tree.getiterator("item")    
                    if bool(self.goodsDetailList) == True : self.goodsDetailList.clear()
                    for item in items:
                        for i in range(9):
                            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find(founds_detail_dic_idx[i]).text))
                            self.goodsDetailList.append((founds_detail_dic_str[founds_detail_dic_idx[i]],item.find(founds_detail_dic_idx[i]).text))
                            
        except Exception:
            print ("※트리 파싱에 에러가 발생하였습니다.※")
        return

    def click_close(self):
        if self.detailOfFoundsXMLDoc != None : self.detailOfFoundsXMLDoc.unlink()
        self.goodsDetailList.clear()
        self.close()
        return
        
    def transmit_email(self):
        self.transmitEmailMenu = MyTransmitEmailMenuForm(None, self.goodsDetailList, None, "습득물")
        self.transmitEmailMenu.show()
        return
        
    def print_image(self):
        global chrome_path
        tree = ElementTree.fromstring(str(self.detailOfFoundsXMLDoc.toxml()))
        items = tree.getiterator("item")    
        for item in items:
            webbrowser.get(chrome_path).open(item.find("fdFilePathImg").text)
        return
        
    def put_on_list(self):
        global foundsDetailBasket
        self.tmpGoodsDetailList = []
        for item in self.goodsDetailList:
            self.tmpGoodsDetailList.append(item)
        foundsDetailBasket.append(self.tmpGoodsDetailList)
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])
        print("바구니에 정보를 담았습니다.")
        return
        
    def transmit_email_list(self):
        global foundsDetailBasket
        global lostsDetailBasket
        self.transmitEmailMenu = MyTransmitEmailMenuForm(None, foundsDetailBasket, lostsDetailBasket, "정보 목록")
        self.transmitEmailMenu.show()
        return
    
    def click_founds_list(self, QModelIndex):
        global foundsDetailBasket
        foundsDetailBasket[QModelIndex.row()].clear()
        foundsDetailBasket.pop(QModelIndex.row())
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        return
        
    def click_losts_list(self, QModelIndex):
        global lostsDetailBasket
        lostsDetailBasket[QModelIndex.row()].clear()
        lostsDetailBasket.pop(QModelIndex.row())
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])     
        return
        
    def preview(self):
        global foundsDetailBasket
        global lostsDetailBasket
        RunPreviewServer(foundsDetailBasket, lostsDetailBasket)
        return
        
    def closeEvent(self, bar):   
        if self.detailOfFoundsXMLDoc != None : self.detailOfFoundsXMLDoc.unlink()
        self.goodsDetailList.clear()
        self.close()
        return

class MyLostsDetailMenuForm(QtGui.QMainWindow):
    goodsDetailList = []
    detailOfLostsXMLDoc = None
    def __init__(self, parent=None, row=0, col=0):
        global informOfLostsXMLDoc
        global founds_DetailBasket
        global losts_DetailBasket
        global item_list
        #global row, col
        QtGui.QWidget.__init__(self, parent)

        self.ui = losts_detail_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])
        
        losts_detail_dic_idx = \
        { 
            0: "lstPrdtNm" , 1 : "lstYmd", 2 : "lstHor", 3: "lstLctNm"  , 4 : "lstPlace",
            5 : "orgId",6: "orgNm" , 7 : "lstSteNm"  , 8 : "tel" , 9 : "uniq"
        }
        losts_detail_dic_str = \
        { 
            "lstPrdtNm" : "물품명 :" , "lstYmd" : "분실 일자 :", "lstHor" : "분실 시간 :", "lstLctNm" : "분실 지역 :"  , "lstPlace" : "분실 장소 :",
            "orgId" : "기관 ID :", "orgNm" : "접수 기관 :" , "lstSteNm" : "분실물 상태 :"  , "tel" : "문의번호 :" , "uniq" : "특이사항 :"
        }
        try:
            tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml())) #ElementTree                       
            items = tree.getiterator("item")  
            for i, item in enumerate(items):
                if i == int(row):
                    #detailURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsDetailInfo?"+"ATC_ID="+item.find("atcId").text + serviceKey
                    detailURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsDetailInfo?"+"ATC_ID="+item_list[i][4] + serviceKey                       
            try:
                xmlFD = urlopen(detailURL)
            except IOError:
                print ("※URL 접근에 실패하였습니다.※")
            else:
                try:
                    self.detailOfLostsXMLDoc = parse(xmlFD)   # XML 문서를 파싱합니다.
                except Exception:
                    print ("※읽어오기가 실패하였습니다.※")
                else:
                    #goodsDetailList = []
                    print ("세부 정보를 출력합니다.")
                    tree = ElementTree.fromstring(str(self.detailOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    if bool(self.goodsDetailList) == True : self.goodsDetailList.clear()
                    for item in items:
                        for i in range(10):
                            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find(losts_detail_dic_idx[i]).text))
                            self.goodsDetailList.append((losts_detail_dic_str[losts_detail_dic_idx[i]],item.find(losts_detail_dic_idx[i]).text))
                            
        except Exception:
            print ("※트리 파싱에 에러가 발생하였습니다.※")
        return

    def click_close(self):
        if self.detailOfLostsXMLDoc != None : self.detailOfLostsXMLDoc.unlink()
        self.goodsDetailList.clear()
        self.close()
        return
        
    def transmit_email(self):
        self.transmitEmailMenu = MyTransmitEmailMenuForm(None, self.goodsDetailList, None, "분실물")
        self.transmitEmailMenu.show()
        return
    def print_image(self):
        global chrome_path
        tree = ElementTree.fromstring(str(self.detailOfLostsXMLDoc.toxml()))
        items = tree.getiterator("item")    
        for item in items:
            webbrowser.get(chrome_path).open(item.find("lstFilePathImg").text)
        return
        
    def put_on_list(self):
        global foundsDetailBasket
        global lostsDetailBasket
        self.tmpGoodsDetailList = []
        for item in self.goodsDetailList:
            self.tmpGoodsDetailList.append(item)
        lostsDetailBasket.append(self.tmpGoodsDetailList)
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])
        print("바구니에 정보를 담았습니다.")
        return
        
    def transmit_email_list(self):
        global foundsDetailBasket
        global lostsDetailBasket
        self.transmitEmailMenu = MyTransmitEmailMenuForm(None, foundsDetailBasket, lostsDetailBasket, "정보 목록")
        self.transmitEmailMenu.show()
        return
        
    def click_founds_list(self, QModelIndex):
        global foundsDetailBasket
        foundsDetailBasket[QModelIndex.row()].clear()
        foundsDetailBasket.pop(QModelIndex.row())
        self.ui.listWidget.clear()
        for founds_list in foundsDetailBasket:
            self.ui.listWidget.addItem(founds_list[0][0]+founds_list[0][1])
        return
        
    def click_losts_list(self, QModelIndex):
        global lostsDetailBasket
        lostsDetailBasket[QModelIndex.row()].clear()
        lostsDetailBasket.pop(QModelIndex.row())
        self.ui.listWidget_2.clear()  
        for losts_list in lostsDetailBasket:
            self.ui.listWidget_2.addItem(losts_list[0][0]+losts_list[0][1])     
        return
    
    def preview(self):
        global foundsDetailBasket
        global lostsDetailBasket
        RunPreviewServer(foundsDetailBasket, lostsDetailBasket)
        return
    
    def closeEvent(self, bar):   
        if self.detailOfLostsXMLDoc != None : self.detailOfLostsXMLDoc.unlink()
        self.goodsDetailList.clear()
        self.close()
        return

class MyFoundsAddrSearchForm(QtGui.QMainWindow):
    pageNum = 1
    addr = None
    founds = None
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = founds_addr_search_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        for i in range(10):
            for j in range(4):
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
        
    def founds_addr_search(self):
        global serviceKey
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("addr").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def founds_print_detail(self, row, col):
        if "-" == (self.ui.tableWidget.item(row, col)).text() : return
        self.foundsDetailMenu = MyFoundsDetailMenuForm(None, row, col)
        self.foundsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("addr").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfFoundsXMLDoc
        global item_list        
        
        item_list.clear()
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("addr").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("addr").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_sort(self):
        global item_list
        sort_list(item_list)
        for i, item in enumerate(item_list):
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item[0]))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item[3]))
        return
        
    def click_back(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.founds = None
        self.addr = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return
        
    def return_to_main(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.founds = None
        self.addr = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.MainMenu = MyMainForm()
        self.MainMenu.show()
        self.close()
        return
        
    def closeEvent(self, bar):   
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.founds = None
        self.addr = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
    
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
        
        for i in range(10):
            for j in range(4):
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
        
    def founds_kind_search(self):
        global serviceKey
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("depPlace").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def founds_print_detail(self, row, col):
        if "-" == (self.ui.tableWidget.item(row, col)).text() : return
        self.foundsDetailMenu = MyFoundsDetailMenuForm(None, row, col)
        self.foundsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("depPlace").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
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
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("fdPrdtNm").text, item.find("fdYmd").text, item.find("depPlace").text, item.find("fdSbjt").text, item.find("atcId").text, item.find("fdSn").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("fdPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("fdYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("depPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("fdSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
        
    def click_sort(self):
        global item_list
        sort_list(item_list)
        for i, item in enumerate(item_list):
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item[0]))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item[3]))
        return
        
    def click_back(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return
    
    def return_to_main(self):
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.MainMenu = MyMainForm()
        self.MainMenu.show()
        self.close()
        return
        
    def closeEvent(self, bar):   
        global informOfFoundsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOFDoc(): informOfFoundsXMLDoc.unlink()
        
        self.close()
        return
        
class MyLostsLocationSearchForm(QtGui.QMainWindow):
    pageNum = 1
    location = None
    losts = None
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = losts_location_search_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        for i in range(10):
            for j in range(4):
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
        
    def losts_location_search(self):
        global serviceKey
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        self.location = self.ui.lineEdit.text()
        self.losts = self.ui.lineEdit_2.text()     
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccTpNmCstdyPlace?"
        optionURL = "LST_PLACE="+quote(self.location)+"&LST_PRDT_NM="+quote(self.losts)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def losts_print_detail(self, row, col):
        if "-" == (self.ui.tableWidget.item(row, col)).text() : return
        self.lostsDetailMenu = MyLostsDetailMenuForm(None, row, col)
        self.lostsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        if not checkIOLDoc(): return
        self.pageNum += 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccTpNmCstdyPlace?"
        optionURL = "LST_PLACE="+quote(self.location)+"&LST_PRDT_NM="+quote(self.losts)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        if not checkIOLDoc(): return
        if self.pageNum == 1 : return        
        self.pageNum -= 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccTpNmCstdyPlace?"
        optionURL = "LST_PLACE="+quote(self.location)+"&LST_PRDT_NM="+quote(self.losts)+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_sort(self):
        global item_list
        sort_list(item_list)
        for i, item in enumerate(item_list):
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item[0]))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item[3]))
        return
    def click_back(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.losts = None
        self.location = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
        self.lostsMenu = MyLostsMenuForm()
        self.lostsMenu.show()
        self.close()
        return
        
    def return_to_main(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.losts = None
        self.location = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
        self.MainMenu = MyMainForm()
        self.MainMenu.show()
        self.close()
        return
        
    def closeEvent(self, bar):   
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.losts = None
        self.location = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
        self.close()
        return
        
class MyLostsKindSearchForm(QtGui.QMainWindow):
    pageNum = 1
    kind = None
    startDay = None
    endDay = None
    items_list = None
    
    def __init__(self, parent=None):
        global kindOfGoodsXMLDoc
        QtGui.QWidget.__init__(self, parent)
        self.ui = losts_kind_search_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.response = kindOfGoodsXMLDoc.childNodes
        self.rsp_child = self.response[0].childNodes
        self.body_list = self.rsp_child[1].childNodes
        self.items = self.body_list[0]
        self.items_list = self.items.childNodes
        
        for i in range(10):
            for j in range(4):
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
        
    def losts_kind_search(self):
        global serviceKey
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        self.kind = (self.items_list[self.ui.comboBox.currentIndex()].childNodes)[0].firstChild.nodeValue
        self.startDay = self.ui.lineEdit.text()
        self.endDay = self.ui.lineEdit_2.text()
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    #print(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    
    def losts_print_detail(self, row, col):
        if "-" == (self.ui.tableWidget.item(row, col)).text() : return
        self.lostsDetailMenu = MyLostsDetailMenuForm(None, row, col)
        self.lostsDetailMenu.show()
        return
        
    def click_next(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        if not checkIOLDoc(): return
        self.pageNum += 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
    def click_prev(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        if not checkIOLDoc(): return
        if self.pageNum == 1 : return        
        self.pageNum -= 1;
        
        basedURL = "http://openapi.lost112.go.kr/openapi/service/rest/LostGoodsInfoInqireService/getLostGoodsInfoAccToClAreaPd?"
        optionURL = "PRDT_CL_CD_01="+self.kind+"&START_YMD="+self.startDay+"&END_YMD="+self.endDay+"&pageNo="+str(self.pageNum)
        totalURL = basedURL+optionURL+serviceKey
        
        print(totalURL)
        
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
                try:
                    tree = ElementTree.fromstring(str(informOfLostsXMLDoc.toxml()))
                    items = tree.getiterator("item")
                    #self.ui.tableWidget.clear()
                    for i in range(10):
                        for j in range(4):
                            self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem("-"))
                    for i, item in enumerate(items):
                        item_list.append((item.find("lstPrdtNm").text, item.find("lstYmd").text, item.find("lstPlace").text, item.find("lstSbjt").text, item.find("atcId").text))
                        self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item.find("lstPrdtNm").text))
                        self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item.find("lstYmd").text))
                        self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item.find("lstPlace").text))
                        self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item.find("lstSbjt").text))
                except Exception:
                    print ("※트리 파싱에 에러가 발생하였습니다.※")
                  
        return
        
    def click_sort(self):
        global item_list
        sort_list(item_list)
        for i, item in enumerate(item_list):
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(item[0]))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(item[3]))
        return
        
    def click_back(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
        self.lostsMenu = MyLostsMenuForm()
        self.lostsMenu.show()
        self.close()
        return
    
    def return_to_main(self):
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
        self.MainMenu = MyMainForm()
        self.MainMenu.show()
        self.close()
        return
        
    def closeEvent(self, bar):   
        global informOfLostsXMLDoc
        global item_list
        
        item_list.clear()
        
        self.kind = None
        self.startDay = None
        self.endDay = None
        self.pageNum = 1
        if checkIOLDoc(): informOfLostsXMLDoc.unlink()
        
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
