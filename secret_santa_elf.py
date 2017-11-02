import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Person:

    def __init__(self, fname, lname, mail_addr):
        self.first_name = fname
        self.last_name = lname
        self.email_addr = mail_addr
        self.no_pair = []
        self.giftee = None

# Get people data from text file

# Create Person object out of each data entry

# Create two lists that each contain all of the people, these will act as stacks
# One will be gifters and one will be giftees

# Shuffle each stack

# Use last person in both lists and give giftee to gifter, if they can't be paired then swap giftee

# Add each gifter to a list

# Send email to each person in the list, telling them their giftee


from_addr = "ianpdegroot@gmail.com"
to_addr = "Address you want to send to"
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "Secret Santa Elf Test Email"
 
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
