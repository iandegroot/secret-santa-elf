import smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Person:

    def __init__(self, fname, lname, mail_addr):
        self.first_name = fname
        self.last_name = lname
        self.email_addr = mail_addr
        self.no_pair = []
        self.giftee = None

    def __str__(self):
        if len(self.no_pair) == 0:
            return "Person:\n{} {}\nGiving a gift to {}\n".format(self.first_name, self.last_name, self.giftee)
        else:
            return "Person:\n{} {}\nCan't give a gift to {}\nGiving a gift to {}\n".format(self.first_name, self.last_name, ", ".join([str(n) for n in self.no_pair]), self.giftee)


def send_email():
    from_addr = "ianpdegroot@gmail.com"
    to_addr = "Address you want to send to"
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = "Secret Santa Elf Test Email"
     
    body = "YOUR MESSAGE HERE"
    msg.attach(MIMEText(body, "plain"))
     
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(from_addr, "P@ssword!")
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
    except:
        print("Something went wrong...")

if __name__ == "__main__":
    master_list = []
    gifters = []
    giftees = []
    # Get people data from text file
    with open(sys.argv[1]) as input_file:
        for line in input_file:
            # Parse people data
            print(line)
            person_data = line.split(", ")
            names = person_data[0].split()
            no_pairs = person_data[2:]

            # Create Person object out of each data entry and store in the master list
            master_list.append(Person(names[0], names[1], person_data[1]))

            # Add people that this person cannot gift to
            if no_pairs[0].strip() != "NA":
                for n in no_pairs:
                    master_list[-1].no_pair.append(n.strip())

            # Push object onto temporary stacks
            gifters.append(master_list[-1])
            giftees.append(master_list[-1])

    for p in master_list:
        print(p)

    # Shuffle each stack

    # Use last person in both lists and give giftee to gifter, if they can't be paired then swap giftee

    # Add each gifter to a list

    # Send email to each person in the list, telling them their giftee