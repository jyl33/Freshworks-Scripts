## This script requires "requests": http://docs.python-requests.org/
## To install: pip install requests
## This script also requires emojis (not really you can delete line 185):
## To install pip install emojis

import random
import requests
import json
import csv
import sys
import getpass
import time
import itertools
import emoji

try:
    import requests
except ImportError:
    sys.exit("""You need requests, go to http://docs.python-requests.org/en/v2.7.0/user/install/ or run the command 'pip install requests' in your terminal""")

csv.field_size_limit(sys.maxsize)

#  ***Edit these***  #
api_key = "jtvGlyYp3fdhYG9xoU3b"
domain = "mozilla-support"
password = "testtest"

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

    data = '{ "name":"%s", "email":"%s" }' %(name,email)
    #print data

    r = requests.post('https://'+str(domain)+'.freshdesk.com/api/v2/contacts', headers=headers, data=data, auth=(api_key, password))

    if r.status_code == 201:
        print "Contact created successfully" #+ r.content
      #print "Location Header : " + r.headers['Location']
    else:
        print "Failed to create contact, errors are displayed below, "
        print "x-request-id : " + r.headers['x-request-id']
        print "Status Code : " + str(r.status_code)

def ticketAutoSubmit(num):
    success = 0
    failed = 0
    i = 0
    print num
    while i < num:
        with open('description.txt') as a:
            reader = csv.reader(a)
            description = random.choice(list(reader))
            description = description[0]
            print description

        with open('email.txt') as b:
            reader = csv.reader(b)
            email = random.choice(list(reader))
            email = email[0]

        with open('priority.txt') as c:
            reader = csv.reader(c)
            priority = random.choice(list(reader))
            priority = priority[0]

        with open('source.txt') as d:
            reader = csv.reader(d)
            source = random.choice(list(reader))
            source = source[0]

        with open('subject.txt') as e:
            reader = csv.reader(e)
            subject = random.choice(list(reader))
            subject = subject[0]

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{ "description": "%s", "subject": "%s", "email": "%s", "priority": '"%s"', "status": 2, "source": '"%s"'}' %(description, subject, email, priority, source)

        response = requests.post('https://'+str(domain)+'.freshdesk.com/api/v2/tickets', headers=headers, data=data, auth=(api_key, password))

        if response.status_code == 201:
            print "success"
            success = success + 1
            i = i+1
        else:
            print "failed, retrying"
            i = i-1
            failed = failed + 1

    print "%s ticket(s) successfully submitted \nLost %s ticket(s) along the way" %(success, failed)

def domain_change():
    global api_key
    global domain
    global password
    domain = raw_input("Enter your domain name: ")
    api_key = raw_input("Enter your email or API key: ")
    password = getpass.getpass("Enter your password: ")

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
                i = raw_input("submit another contact? (y/n)")
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

#this function controls the frequency and number of tickets submitted
def auto_submit():
    delay = 1
    count = 0
    minutes = 3 #Edit this value to edit the time between ticket submissions
    seconds = minutes * 60

    start = time.time()
    while True:
        random_number = random.randint(10,15)
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
        else:
            print "%s seconds have passed, %s tickets submitted so far" %(round(time.time()-start,2), count)

        print "sleeping for %s minutes..." %minutes,

        print(emoji.emojize(':sleeping:', use_aliases=True))

        time.sleep(seconds - ((time.time() - start) % seconds))



def prompt_user():
    choice = raw_input("\nPlease enter a value: \nAdd contacts (m)anually, or (r)ead from file.\nAdd (t)ickets, or add (s)olutions articles \nChanges will be made to " + color.RED + domain + color.END + ".freshdesk.com. (c)hange domain \n")

    if choice == ("m" or "M"):
        manual_contact()

    elif choice == ("r" or "R"):
        contacts_file = raw_input("Enter the name of the file to read [Case Sensitive]: ")
        file_contacts(contacts_file)

    elif choice == ("t" or "T"):
        mode = raw_input("(C)ontinuous submission or (o)ne time?: ")
        if mode == ("c" or "C"):
            print "Beginning continuous submission of tickets..."
            auto_submit()
        elif mode == ("o" or "O"):
            num = int(input("How many tickets would you like to submit?: "))
            ticketAutoSubmit(num)
        prompt_user()

    elif choice == ("c" or "C"):
        domain_change()
        prompt_user()

    elif choice == ("s" or "S"):
        num = raw_input("How many solutions articles do you want to submit? ")
        article_submit(num)

prompt_user()
