import sys

from PyQt4 import QtGui, QtCore

import transmit_email_menu_ui

from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

LDB = []
FDB = []

host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

class MyTransmitEmailMenuForm(QtGui.QMainWindow):
    #goodsDetailList = []
    def __init__(self, parent=None, foundsDetailList = None, lostsDetailList = None, about = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = transmit_email_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        
        self.foundsDetailList = []
        self.lostsDetailList = []
        
        for item in foundsDetailList:
                self.foundsDetailList.append(item)
                
        if lostsDetailList != None:
            for item in lostsDetailList:
                self.lostsDetailList.append(item)
        else :
            self.lostsDetailList = None
        self.about = about

    def transmit_email(self):
        global host, port
        html = ""

        if self.lostsDetailList == None:
            html = MakeHtmlDoc(self.foundsDetailList, self.about)
        else :
            html = MakeHtmlDocDetail(self.foundsDetailList, self.lostsDetailList, self.about)
        title = self.ui.lineEdit.text()
        senderAddr = self.ui.lineEdit_2.text()
        passwd = self.ui.lineEdit_3.text()
        recipientAddr = self.ui.lineEdit_4.text() 
        
        import smtplib                               #python3.5에서는 smtplib 사용해도 됨
        from email.mime.multipart import MIMEMultipart #MIMEMultipart MIME 생성
        from email.mime.text import MIMEText
        msg = MIMEMultipart('alternative') #Message container를 생성
        msg['Subject'] = title          #set message
        msg['From'] = senderAddr
        msg['To'] =  recipientAddr

        goodsDetailPart = MIMEText(html, 'html', _charset = 'UTF-8') 
        

        msg.attach(goodsDetailPart)  
        print ("SMTP 서버에 연결 중 ... ")
        s = smtplib.SMTP(host,port) #python3.5에서는 smtplib.SMTP(host,port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(senderAddr, passwd)    # 로그인  
        s.sendmail(senderAddr , [recipientAddr], msg.as_string())
        s.close()    
        print ("메일을 전송하였습니다.")
        
        self.close()
        return
        
def MakeHtmlDoc(goodsDetailList, about):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  #dom 객체 생성
    top_element = newdoc.documentElement # 해당 dom객체의 엘리먼트 객체 반환
    header = newdoc.createElement('header') #dom 객체로부터 엘리먼트 생성
    top_element.appendChild(header) #top_element 엘리먼트의 자식으로 header 엘리먼트 추가

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')
    
    p = newdoc.createElement('p')
    titleText = newdoc.createTextNode("'{0}'에 대한 상세 정보입니다.".format(about))
    p.appendChild(titleText)
    body.appendChild(p)

    for goodsDetailItem in goodsDetailList:
        #create bold element
        b = newdoc.createElement('b')
        #create text node
        keyText = newdoc.createTextNode(goodsDetailItem[0])
        b.appendChild(keyText)
        body.appendChild(b)
        
        msgText = newdoc.createTextNode(goodsDetailItem[1])
        body.appendChild(msgText)
        br = newdoc.createElement('br')
        body.appendChild(br)
         
    #append Body
    top_element.appendChild(body)
    print("첨부 완료")
    return newdoc.toxml()

def MakeHtmlDocDetail(foundsDetailBasket, lostsDetailBasket, about):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  #dom 객체 생성
    top_element = newdoc.documentElement # 해당 dom객체의 엘리먼트 객체 반환
    header = newdoc.createElement('header') #dom 객체로부터 엘리먼트 생성
    top_element.appendChild(header) #top_element 엘리먼트의 자식으로 header 엘리먼트 추가

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')
    
    p = newdoc.createElement('p')    
    titleText = newdoc.createTextNode("'{0}'에 대한 상세 정보입니다.".format(about))
    p.appendChild(titleText)
    body.appendChild(p)
    
    p = newdoc.createElement('p')
    titleText = newdoc.createTextNode("<습득물 상세 정보 리스트>")
    p.appendChild(titleText)
    body.appendChild(p)

    for i, goodsDetailList in enumerate(foundsDetailBasket):
        p = newdoc.createElement('p')
        idxText = newdoc.createTextNode('[{0}]'.format(i+1))
        p.appendChild(idxText)
        body.appendChild(p)     
        for goodsDetailItem in goodsDetailList:
            b = newdoc.createElement('b')
            #create text node
            keyText = newdoc.createTextNode(goodsDetailItem[0])
            b.appendChild(keyText)
            body.appendChild(b)
            
            msgText = newdoc.createTextNode(goodsDetailItem[1])
            body.appendChild(msgText)
            br = newdoc.createElement('br')
            body.appendChild(br)
        #append Body
        br = newdoc.createElement('br')
        body.appendChild(br)
    #top_element.appendChild(body)
    br = newdoc.createElement('br')
    body.appendChild(br)
    body.appendChild(br)
    
    p = newdoc.createElement('p')
    titleText = newdoc.createTextNode("<분실물 상세 정보 리스트>")
    p.appendChild(titleText)
    body.appendChild(p)

    for i, goodsDetailList in enumerate(lostsDetailBasket):
        p = newdoc.createElement('p')
        idxText = newdoc.createTextNode('[{0}]'.format(i+1))
        p.appendChild(idxText)
        body.appendChild(p)     
        for goodsDetailItem in goodsDetailList:
            b = newdoc.createElement('b')
            #create text node
            keyText = newdoc.createTextNode(goodsDetailItem[0])
            b.appendChild(keyText)
            body.appendChild(b)
            
            msgText = newdoc.createTextNode(goodsDetailItem[1])
            body.appendChild(msgText)
            br = newdoc.createElement('br')
            body.appendChild(br)
        #append Body
        br = newdoc.createElement('br')
        body.appendChild(br)
        
    top_element.appendChild(body)
        
    print("첨부 완료")
    return newdoc.toxml()


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global FDB
        global LDB
        html = MakeHtmlDocDetail(FDB, LDB, "정보 목록") # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
        ##헤더 부분을 작성.
        print(html)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('euc-kr')) #  본분( body ) 부분을 출력 합니다.

def RunPreviewServer(mFDB, mLDB):
    global FDB
    global LDB
    
    for item in mFDB:
        FDB.append(item)
    for item in mLDB:
        LDB.append(item)
        
    import webbrowser
    server = HTTPServer( ('localhost',8080), ServerHandler)
    print("미리 보기")
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("http://localhost:8080/?")
    server.handle_request()
    server.socket.close()
    FDB.clear()
    LDB.clear()
        
        
