import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from_addr = "ianpdegroot@gmail.com"
to_addr = "ADDRESS YOU WANT TO SEND TO"
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "SUBJECT OF THE MAIL"
 
body = "YOUR MESSAGE HERE"
msg.attach(MIMEText(body, 'plain'))
 
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(from_addr, "P@ssword!")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
except:
    print "Something went wrong..."
