import sys

from PyQt4 import QtGui, QtCore

import transmit_email_menu_ui

host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

class MyTransmitEmailMenuForm(QtGui.QMainWindow):
    #goodsDetailList = []
    def __init__(self, parent=None, goodsDetailList = None, about = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = transmit_email_menu_ui.Ui_Form()
        self.ui.setupUi(self)
        self.goodsDetailList = []
        for item in goodsDetailList:
            self.goodsDetailList.append(item)
        self.about = about

    def transmit_email(self):
        global host, port
        html = ""

        html = MakeHtmlDoc(self.goodsDetailList, self.about)
        
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
        self.goodsDetailList.clear()
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
        br = newdoc.createElement('br')
        
        b = newdoc.createElement('b')
        #create text node
        keyText = newdoc.createTextNode(goodsDetailItem[0])
        b.appendChild(keyText)
        body.appendChild(b)
        
        msgText = newdoc.createTextNode(goodsDetailItem[1])
        body.appendChild(msgText)
        
        body.appendChild(br)
        body.appendChild(br)
         
    #append Body
    top_element.appendChild(body)
    print("첨부 완료")
    return newdoc.toxml()