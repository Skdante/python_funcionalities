import os
import smtplib
import mimetypes
import email.mime.application
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fnSendEmail(objCFG):
    try:
        objSMTP = smtplib.SMTP('50.207.44.37', 587)
        objSMTP.login('sqljmail', 'Pr1mu$1@b$')
        objMessage = MIMEMultipart()
    
        strSubject = objCFG.get("subject", '')
        strFromEmail = objCFG.get("from",'')
        strToEmail = objCFG.get("to",'')
        strBodyEmail = objCFG.get("body",'')
        strHTMLBody = objCFG.get("html",'')
    
        if strSubject == '':
            print('---|||||| ERROR: Provide subject ||||||---')
            return False    
        if strFromEmail == '':
            print('---|||||| ERROR: Provide from email ||||||---')
            return False 
        if strToEmail == '':
            print('---|||||| ERROR: Provide to email ||||||---')
            return False  
        if strBodyEmail == '':
            if strHTMLBody == '':
                print('---|||||| ERROR: Provide body message ||||||---')
                return False
            else: 
                objMessage.attach(MIMEText(strHTMLBody,'html'))
                            
        objMessage['Subject'] = strSubject
        objMessage['From'] = strFromEmail
        objMessage['To'] = strToEmail

        strCCEmail = objCFG.get('cc','')
        strBCCEmail = objCFG.get('bcc','')
            
        if strCCEmail != '': 
            objMessage['Cc'] = strCCEmail

        if strBCCEmail != '': 
            objMessage['Bcc'] = strBCCEmail               
        
        objMessage.attach(MIMEText(strBodyEmail))
        
        arrFiles = objCFG.get('files',None)
        if arrFiles != None:
            for strFileName in arrFiles:
                extension = os.path.splitext(strFileName)[1][1:]
                objFile =open(strFileName,'rb')
                objAttach = email.mime.application.MIMEApplication(objFile.read(),_subtype=extension)
                objFile.close()
                objAttach.add_header('Content-Disposition','attachment',filename=strFileName)
                objMessage.attach(objAttach)
        objSMTP.send_message(objMessage)
        objSMTP.quit()
    except Exception as e:
         print("---|||||| ERROR: Azzule Send Email {0} ||||||---".format(e))
    return True