import smtplib, sys, random
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

    # Return True if and only if the passed in name is not in the no_pair list
    def can_gift(self, name):
        for cannot_gift_name in self.no_pair:
            if name == cannot_gift_name:
                return False
        return True



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
            # Skip commented and empty lines
            if line.startswith("#") or not line.split():
                continue
            # Parse people data
            print(line)
            person_data = line.split(";")
            if (len(person_data) != 4):
                print("ERROR: The following line of the input text file was not formatted correctly:")
                print("\t", line)
                sys.exit()
            # Split first and last name
            names = person_data[0].split()
            email = person_data[1]

            # Create Person object out of each data entry and store in the master list
            master_list.append(Person(names[0], names[1], email))

            # Check for people that this person cannot gift to
            #if len(person_data) > 2:
            no_pairs = person_data[2].strip()
                #if len(person_data) > 3:
            giftee = person_data[3].strip()
            # if giftee != "NA":
            #     master_list[-1].giftee = giftee

            # Add people that this person cannot gift to
            if no_pairs != "NA":
                for n in no_pairs.split(","):
                    master_list[-1].no_pair.append(n.strip())
            # Add themseleves to the list of people they can't gift to
            master_list[-1].no_pair.append(master_list[-1].first_name + " " + master_list[-1].last_name)


            # Push object onto temporary stacks
            gifters.append(master_list[-1])
            giftees.append(master_list[-1])

    # Shuffle each stack
    random.shuffle(gifters)
    random.shuffle(giftees)

    # Use last person in both lists and give giftee to gifter, if they can't be paired then swap giftee
    for _ in range(len(gifters)):
        gifter = gifters[-1]
        giftee = giftees[-1]

        no_match_found = True
        alt_giftee_index = 0

        while no_match_found:
            no_match_found = False
            if not gifter.can_gift(giftee.first_name + " " + giftee.last_name):
                if len(gifters) == 1:
                    print("Sucks to suck!!!")
                else:
                    # Get a new giftee, - 2 so that the same giftee can't be selected
                    alt_giftee_index = random.randint(0, len(gifters) - 2)
                    giftees[-1], giftees[alt_giftee_index] = giftees[alt_giftee_index], giftees[-1]
                    giftee = giftees[-1]
                    no_match_found = True
                    print("Bad pair found!!!!")


        gifter.giftee = giftee.first_name + " " + giftee.last_name

        gifters.pop()
        giftees.pop()

    # Send email to each person in the list, telling them their giftee
    for p in master_list:
        print(p)
