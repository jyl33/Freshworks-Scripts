## This script requires "requests": http://docs.python-requests.org/
## To install: pip install requests
import random
import requests
import json
import csv
import sys
import getpass
import time
import emoji

try:
    import requests
except ImportError:
    sys.exit("""You need requests, go to http://docs.python-requests.org/en/v2.7.0/user/install/ or run the command 'pip install requests' in your terminal""")


csv.field_size_limit(sys.maxsize)

api_key = "lOdmIwElEiEFHwjQLUUs"
domain = "polloshermanos"
password = "password" #No need to edit this

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def send_it(name,email):
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{ "user":{"name":"%s", "email":"%s"} }' %(name,email)
    #print data

    r = requests.post('https://'+str(domain)+'.freshservice.com/itil/requesters.json', headers=headers, data=data, auth=(api_key, password))

    if r.status_code == 201 or 200:
        print "Contact created successfully"
    else:
        print "Failed to create contact, errors are displayed below, "
        print "x-request-id : " + r.headers['x-request-id']
        print "Status Code : " + str(r.status_code)

def ticketAutoSubmit(num):
    success = 0
    failed = 0
    i = 0
    while i < num:
        with open('descriptions.txt') as a:
            reader = csv.reader(a)
            description = random.choice(list(reader))
            description = description[0]

        with open('emails.txt') as b:
            reader = csv.reader(b)
            email = random.choice(list(reader))
            email = email[0]

        with open('priorities.txt') as c:
            reader = csv.reader(c)
            priority = random.choice(list(reader))
            priority = priority[0]

        with open('sources.txt') as d:
            reader = csv.reader(d)
            source = random.choice(list(reader))
            source = source[0]

        with open('subjects.txt') as e:
            reader = csv.reader(e)
            subject = random.choice(list(reader))
            subject = subject[0]

        with open('types.txt') as f:
            reader = csv.reader(f)
            type_ = random.choice(list(reader))
            type_ = type_[0]

        with open('frequency.txt') as g:
            reader = csv.reader(g)
            freq = random.choice(list(reader))
            freq = freq[0]



        print("Submitting ticket number {}...".format(i+1)),
        i = i+1


        headers = {
            'Content-Type': 'application/json',
        }

        data = '{ "helpdesk_ticket":{"description": "%s", "subject": "%s", "email": "%s", "priority": '"%s"', "status": 2, "source": '"%s"', "custom_field": { "type_194465": "%s", "how_long_have_you_had_this_issue_194465":"%s"} } }' %(description, subject, email, priority, source, type_, freq)

        response = requests.post('https://'+str(domain)+'.freshservice.com/helpdesk/tickets.json', headers=headers, data=data, auth=(api_key, password))
        #print response.status_code

        if response.status_code == 201 or 200:
            print "success"
            success = success + 1
        else:
            print "failed, %s retrying" %response.status_code
            i = i-1
            failed = failed + 1

        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

    print "%s ticket(s) successfully submitted \nLost %s ticket(s) along the way" %(success, failed)

def domain_change():
    global api_key
    global domain
    global password
    domain = raw_input("Enter your domain name: ")
    api_key = raw_input("Enter your email or API key: ")
    password = "password"

    headers = {
            'Content-Type': 'application/json',
        }

    r = requests.get('https://'+str(domain)+'.freshdesk.com/api/v2/tickets/1', headers = headers, auth = (api_key, password))

    if r.status_code != 200:
        print "Could not authenticate, please try again"
        domain_change()

def manual_contact():
    while True:
            bool = True
            name = raw_input("enter a name: ")
            email = raw_input("enter an email: ")
            send_it(name,email)
            while bool:
                i = raw_input("submit another contact? (y/n): ")
                if i.strip() == ("n" or "N"):
                    prompt_user()
                elif i.strip() == ("y" or "Y"):
                    bool = False
                else:
                    continue

def file_contacts(contacts_file):
    try:
        with open(contacts_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print row[0] + ", "+ row[1]
                name=row[0]
                email=row[1]
                send_it(name,email)
    except IOError:
        print "Could not find %s" %contacts_file
        prompt_user()

    prompt_user()

#This method handles the ticket submission.
def auto_submit(num):
    count = 0
    start = time.time()
    minutes = 3 #Edit this value to edit the time between ticket submissions
    seconds = minutes * 60

    while True:
        random_number = random.randint(3,15) #(x,y) represents a random number between x and y. Edit this to your liking
        print "\nSubmitting %s tickets" %random_number
        ticketAutoSubmit(random_number)
        count = count + random_number
        if time.time()-start >= 60.0:
            mins = ((time.time()-start) / 60)
            if mins >= 60:
                mins = mins/60
                print "%s hour(s) have passed, %s tickets submitted so far" %(round(mins,2), count)
            else:
                print "%s minutes have passed, %s tickets submitted so far" %(round(mins,2), count)
                if num != 0:
                    if (round(mins,2) > num):
                        prompt_user()
        else:
            print "%s seconds have passed, %s tickets submitted so far" %(round(time.time()-start,2), count)



        print "sleeping for %s minutes..." %minutes,

        print(emoji.emojize(':sleeping:', use_aliases=True))

        time.sleep(seconds - ((time.time() - start) % seconds)) #Edit the numbers to edit the sleep time. 120.0 = 2 minutes


def resolveTickets():
    headers = { 'Content-Type' : 'application/json' }

    ticket = {"helpdesk_ticket": { 'status': 4 }}

    start = input("Enter ticket range start: ")
    end = input("Enter ticket range end: ")

    for ticket_id in range (start, end):
        r = requests.put("https://polloshermanos.freshservice.com/helpdesk/tickets/"+str(ticket_id)+".json", auth = (api_key, password), headers = headers, data = json.dumps(ticket))
        print "updating ticket %s..." %(ticket_id),

        if r.status_code == 200 or 201:
            print "success"
        else:
            print "failed"

        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

    print ("All done")

def prompt_user():
    choice = raw_input("\nPlease enter a value: \nAdd contacts (m)anually, or (r)ead from file.\nAdd (t)ickets, (u)pdate tickets\nChanges will be made to " + color.CYAN     + domain + color.END + ".freshservice.com.\n(c)hange domain \n")

    if choice == ("m" or "M"):
        manual_contact()

    elif choice == ("r" or "R"):
        contacts_file = raw_input("Enter the name of the file to read [Case Sensitive]: ")
        file_contacts(contacts_file)

    elif choice == ("t" or "T"):
        mode = raw_input("(C)ontinuous submission or (o)ne time?: ")
        if mode == ("c" or "C"):
            time = raw_input("(I)ndefinitely or time (b)ased?: ")
            if time == ("i" or "I"):
                print "Beginning continuous submission of tickets..."
                auto_submit(0)
            elif time == ("b" or "B"):
                print "hit"
                num = int(input("How many minutes of continuous submission?: "))
                print "Beginning %s minutes of ticket submission" %num
                auto_submit(num)
        elif mode == ("o" or "O"):
            num = int(input("How many tickets would you like to submit?: "))
            ticketAutoSubmit(num)
        prompt_user()

    elif choice == ("c" or "C"):
        domain_change()
        prompt_user()

    elif choice == ("u" or "U"):
        resolveTickets();

prompt_user()
