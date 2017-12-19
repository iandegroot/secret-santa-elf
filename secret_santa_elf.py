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
        self.forced_gifter = False
        self.forced_giftee = False

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



def send_email(person, email, password):
    from_addr = email
    to_addr = person.email_addr
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = "Secret Santa Assignment!"

    html = """\
            <html>
              <head></head>
              <body>
                <pre style="font-size: 130%">
                      / \\
                     /   \\
                    /_____\\
                  {{`_______`}}
                   // . . \\\\
                  (/   *   \\)
                  |'-' = `-'|
                  |         |
                  /\\       /\\
                 /  `.   .`  \\
                /_/   \\*/   \\_\\
               {{__}}###[_]###{{__}}
               (_/\\_________/\\_)
                   |___|___|
                    |--|--|
                   (__)`(__)
                </pre>
                <p>Hey {}!<br>
                   <br>
                   For Secret Santa this year you'll be giving {} {} a present. Make sure you get them something good!<br>
                   <br>
                   XOXOXOX,<br>
                   Santa's Elf
                </p>
              </body>
            </html>
            """.format(person.first_name, person.giftee.first_name, person.giftee.last_name)

    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(True)
        # server.ehlo()
        server.starttls()
        server.login(from_addr, password)
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

            # Get the list of people that this person cannot gift to
            no_pairs = person_data[2].strip()

            # Set giftee to a gifter
            giftee = person_data[3].strip()
            if giftee != "NA":
                master_list[-1].forced_gifter = True
                master_list[-1].giftee = giftee

            # Add people that this person cannot gift to
            if no_pairs != "NA":
                for n in no_pairs.split(","):
                    master_list[-1].no_pair.append(n.strip())

            # Add themseleves to the list of people they can't gift to
            master_list[-1].no_pair.append(master_list[-1].first_name + " " + master_list[-1].last_name)


def assign_giftees_to_gifters(everyone):
    gifters = []
    giftees = []

    # Push people onto two temporary stacks, everyone will be a gifter and a giftee unless they're designated as a forced gifter or giftee
    for person in everyone:
        if not person.forced_gifter:
            gifters.append(person)
        if not person.forced_giftee:
            giftees.append(person)

    # Make sure that the two stacks are equal in length
    if len(gifters) != len(giftees):
        print("ERROR: The number of gifters does not match the number of giftees (after resloving forced assignments). Exiting the program.")
        sys.exit()

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
            # Check if the gifter can give to the selected giftee, if they can then skip this block
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

        # Assign giftee to gifter
        curr_gifter.giftee = curr_giftee

        # Pop both the gifter and giftee out of their respective stacks
        gifters.pop()
        giftees.pop()

    return True

def find_forced_giftees(everyone):

    # Find giftee in giftees stack, assign person object to the gifter instead of just the name, and remove the giftee from the stack
    for gifter in everyone:
        # Find the gifters who already have a forced assignment
        if gifter.forced_gifter:
            # Check through all the giftees to find the name of the forced assignment
            found_giftee = False
            for giftee in everyone:
                if gifter.giftee == giftee.first_name + " " + giftee.last_name:
                    gifter.giftee = giftee
                    giftee.forced_giftee = True
                    found_giftee = True
                    break
            if not found_giftee:
                print("ERROR: Did not find person " + gifter.giftee + " that " + gifter.first_name + " " + gifter.last_name + " was supposed to give to.")
                print("Please check the spelling and try again.")
                print("Exiting the program.")
                sys.exit()


if __name__ == "__main__":
    master_list = []

    ##### Parse People Data From Text File #####
    parse_input_file(master_list, sys.argv[1])

    ##### Check for Forced Assignments #####
    find_forced_giftees(master_list)

    ##### Give Out Assignments #####
    redo_cntr = 0
    assigning_results = assign_giftees_to_gifters(master_list)

    # If the giftees were successfully assigned, call assign_giftees_to_gifters until they are
    while not assigning_results:
        redo_cntr += 1
        assigning_results = assign_giftees_to_gifters(master_list)

    # for p in master_list:
    #     print(p)

    ##### Send Emails #####
    if assigning_results:
        print("Gave out successful assignments!")
        print("Redo counter:", redo_cntr)
    else:
        print("Didn't give out successfully assignments... Exiting the program, please try again.")
        sys.exit()

    answer = input("Would you like to email the generated assignments? (y/n):\n").lower()
    while answer != "y" and answer != "n":
        answer = input("Invalid input. Please enter either y or n.\nWould you like to email the generated assignments? (y/n):\n")

    if answer == "y":
        email = input("Please enter the email you'd like to send the assignments from:\n")
        password = getpass.getpass("Please enter the password of this email:\n")
        for p in master_list:
            #print(p)
            send_email(p, email, password)
