import smtplib, sys, random, getpass
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
        giftee_print = ""
        if isinstance(self.giftee, Person):
            giftee_print = self.giftee.first_name + " " + self.giftee.last_name
        else:
           giftee_print = self.giftee 


        if len(self.no_pair) == 0:
            return "Person:\n{} {}\nGiving a gift to {}\n".format(self.first_name, self.last_name, giftee_print)
        else:
            return "Person:\n{} {}\nCan't give a gift to {}\nGiving a gift to {}\n".format(self.first_name, self.last_name, ", ".join([str(n) for n in self.no_pair]), giftee_print)

    # Return True if and only if the passed in name is not in the no_pair list
    def can_gift(self, name):
        for cannot_gift_name in self.no_pair:
            if name == cannot_gift_name:
                return False
        return True



def send_email(person):
    from_addr = "ianpdegroot@gmail.com"
    to_addr = person.email_addr
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = "Secret Santa Elf Test Email"

    ascii_santa = ""
    ascii_santa += "          / \\" + "\n"
    ascii_santa += "         /   \\" + "\n"
    ascii_santa += "        /_____\\" + "\n"
    ascii_santa += "      {`_______`}" + "\n"
    ascii_santa += "       // . . \\\\" + "\n"
    ascii_santa += "      (/   *   \\)" + "\n"
    ascii_santa += "      |'-' = `-'|" + "\n"
    ascii_santa += "      |         |" + "\n"
    ascii_santa += "      /\\       /\\" + "\n"
    ascii_santa += "     /  `.   .`  \\" + "\n"
    ascii_santa += "    /_/   \\*/   \\_\\" + "\n"
    ascii_santa += "   {__}###[_]###{__}" + "\n"
    ascii_santa += "   (_/\\_________/\\_)" + "\n"
    ascii_santa += "       |___|___|" + "\n"
    ascii_santa += "        |--|--|" + "\n"
    ascii_santa += "       (__)`(__)" + "\n"

    html = """\
            <html>
              <head></head>
              <body>
                <p>Hey {}!<br>
                   How are you?<br>
                   For Secret Santa this year you'll be giving {} {} a present. Make sure you get them something good!<br>
                   Here is the <a href="http://www.python.org">link</a> you wanted.<br>
                   {}<br>
                   XOXOXOX,\nSanta's Elf
                </p>
              </body>
            </html>
            """.format(person.first_name, person.giftee.first_name, person.giftee.last_name, ascii_santa)
     
    body = "Hey {}!\n\nFor Secret Santa this year you'll be giving {} {} a present. Make sure you get them something good!\n\n {} \n\nXOXOXOX,\nSanta's Elf".format(person.first_name, person.giftee.first_name, person.giftee.last_name, ascii_santa)
    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html, "html"))

     
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(True)
        # server.ehlo()
        server.starttls()
        server.login(from_addr, "add_password_here")
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
    except Exception as e:
        print(e)


def parse_input_file(everyone, filename):
    # Fill the master list with people from the input file
    with open(filename) as input_file:
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


def assign_giftees_to_gifters(everyone):
    gifters = []
    giftees = []

    # Push people onto two temporary stacks, everyone will be a gifter and a giftee
    for person in everyone:
        gifters.append(person)
        giftees.append(person)

    # Shuffle each stack
    random.shuffle(gifters)
    random.shuffle(giftees)

    # Use last person in both lists and give giftee to gifter, if they can't be paired then swap giftee
    for _ in range(len(gifters)):
        curr_gifter = gifters[-1]
        curr_giftee = giftees[-1]

        no_match_found = True
        alt_giftee_index = 0
        num_new_giftees_tried = 0

        # Find a giftee for each gifter
        while no_match_found:
            no_match_found = False
            # Check if the gifter can't give to the selected giftee, if they can then skip this block
            if not curr_gifter.can_gift(curr_giftee.first_name + " " + curr_giftee.last_name):
                # If not, check if this is a special case:
                # The gifter cannot give to any of the giftees that are left
                if len(gifters) == 1 or num_new_giftees_tried > 2:
                    # Restart the whole process
                    return False
                else:
                    # Get a new giftee, - 2 so that the same giftee can't be selected
                    alt_giftee_index = random.randint(0, len(gifters) - 2)
                    # Swap new giftee with the current giftee at the top of the stack
                    giftees[-1], giftees[alt_giftee_index] = giftees[alt_giftee_index], giftees[-1]
                    curr_giftee = giftees[-1]
                    # Now go back and check if the gifter can give to the new giftee
                    no_match_found = True
                    num_new_giftees_tried += 1
                    print("Bad pair found!!!!")

        curr_gifter.giftee = curr_giftee

        gifters.pop()
        giftees.pop()

    return True

if __name__ == "__main__":
    master_list = []

    ##### Get people data from text file #####
    parse_input_file(master_list, sys.argv[1])

    ##### Give out assignments #####
    redo_cntr = 0
    assigning_results = assign_giftees_to_gifters(master_list)

    while not assigning_results:
        print("Redoing assignments!!!")
        redo_cntr += 1
        assigning_results = assign_giftees_to_gifters(master_list)

    ##### Send email to each person in the list, telling them who they need to give a gift to #####
    for p in master_list:
        print(p)

    if assigning_results:
        print("Gave out successful assignments!")
        print("Redo counter:", redo_cntr)
    else:
        print("Didn't give out successfully assignments... Please try again")

    answer = input("Would you like to email the generated assignments? (y/n):\n").lower()
    while answer != "y" and answer != "n":
        answer = input("Invalid input.\nWould you like to email the generated assignments? (y/n):\n")

    if answer == "y":
        #email = input("Please enter the email you'd like to send the assignments froms:\n")
        #password = getpass.getpass("Please enter the password of this email:\n")
        send_email(master_list[0])
        # for p in master_list:
        #     send_email(p)
