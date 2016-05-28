# -*- coding: utf-8 -*-
"""
Created on Sat May 28 15:29:02 2016

@author: 심정환PC
"""

host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

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

def sendMain(goodsDetailList, about):
    global host, port
    print("다음의 메일 양식을 작성해주세요.")
    html = ""
    title = str(input ('제목 :'))
    senderAddr = str(input ('보내는 메일 주소 :'))
    recipientAddr = str(input ('받는 메일 주소 :'))
    msgtext = str(input ('내용 :'))
    passwd = str(input ('보내는 메일 주소의 비밀번호 :'))
    msgtext = str(input ('상세정보 내용을 추가할까요? (y/n):'))
    if msgtext == 'y' :
        #keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(goodsDetailList, about)
    
    import smtplib                               #python3.5에서는 smtplib 사용해도 됨
    from email.mime.multipart import MIMEMultipart #MIMEMultipart MIME 생성
    from email.mime.text import MIMEText
    msg = MIMEMultipart('alternative') #Message container를 생성
    msg['Subject'] = title         #set message
    msg['From'] = senderAddr
    msg['To'] = recipientAddr  
    msgPart = MIMEText(msgtext, 'plain')  
    goodsDetailPart = MIMEText(html, 'html', _charset = 'UTF-8') 
    
    msg.attach(msgPart) # 메세지에 생성한 MIME 문서를 첨부합니다
    msg.attach(goodsDetailPart)  
    print ("SMTP 서버에 연결 중 ... ")
    s = smtplib.SMTP(host,port) #python3.5에서는 smtplib.SMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로그인  
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()    
    print ("메일을 전송하였습니다.")

