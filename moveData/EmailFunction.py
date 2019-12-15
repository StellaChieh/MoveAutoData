# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


class Email:

    def __init__(self, sender='cmt@cwb.gov.tw', smtp_server='ms.mic.cwb'):
        self.sender = sender
        self.smtp_server = smtp_server

    def send_email(self, receiver_list, subject, message, attach_file_list=None):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ', '.join(receiver_list)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        
        # get all the attachments
        if attach_file_list is not None:
            for attach_file in attach_file_list:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attach_file, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename='+attach_file)
                msg.attach(part)         

        smtp = None
        try:
            smtp = smtplib.SMTP(self.smtp_server)
            smtp.sendmail(self.sender, receiver_list, msg.as_string())
            print 'Successfully sent email.'
        except smtplib.SMTPException as err:
            print 'Sent email failed!'
            raise err
        finally:
            if smtp is not None:
                smtp.quit()
        

if __name__ == '__main__':
    e = Email()
    e.send_email(['stella.chieh@iisigroup.com', 'stella.chieh@gmail.com'], '主題', '內容')