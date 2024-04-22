"""Takes an ASM delete ticket and automatically generates an email to the manager in question
TO DO:
-Edit existing .eml file rather than writing each time.
-Search for correct location of values in ticket rather than using magic numbers.
"""

import sys
import os
from datetime import date
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
file_path = "C:/Users/burrellq/OneDrive - education.govt.nz/Documents/scripts/Delete Auto Mail/"

"""Takes an input as a pasted ticket and outputs it as a string"""
def read_ticket():
    print("Paste the ticket here then hit ctrl-z:\n")
    ticket = sys.stdin.read()
    return(ticket)

"""Takes a ticket as a string and extracts details from it
Outputs details as req_num, user, manager, date
assumes positions in ASM ticket as determined by set values user_x etc."""
def extract(ticket, user_x=35, manager_x=9, date_x=93): #some more magic numbers. The location of the values to be extracted.
    user_x = ticket[0].find('r ') + 2
    user_y = ticket[0].find('.')
    user = ticket[0][user_x:user_y] #slices the users name
    
    manager_x = ticket[1].find(': ') + 2
    manager = ticket[1][manager_x:].strip()    #slices managers name
    
    date_x = ticket[0].find('ve ') + 3
    end_date = ticket[0][date_x:].strip()   #slices the end date
    
    return user, manager, end_date

"""converts the end_date as an int in YYYYMMDD format, then checks it 
against the current date to return a boo for if end date is in the past"""
def past(end_date):
    int_date = int(end_date[-4:] + end_date[3:5] + end_date[0:2])
    past = int_date < int(str(date.today()).replace("-", ""))
    return past

"""Takes a name and outputs a MoE email address from that name"""
def emailise(name, email_name=""):
    for c in name:
        if c.isalpha():
            email_name += c
        if c == " ":
            email_name += "."
    return email_name + "@education.govt.nz"

"""Inserts the user's name, manager's first name, and end date from the ticket into a block of html text that will be the email."""
def email_text(user, manager_first, end_date):
    past_text = ["is leaving", "has left"]
    return f"""
    Kia ora {manager_first},<br>
    <br>
    Service Desk have been notified by People Services that your staff member {user} {past_text[past(end_date)]} the Ministry on {end_date}.<br>
    <br>
    If this is not correct please respond to this email to advise.<br>
    <br>
    •	For security reasons, if a staff member is leaving the Ministry, it is important to submit a Delete User Account request form, which will ensure that the Ministry will not be in breach of Security and Audit requirements. <br>
    •	If your staff member has been re-employed or has been made permanent and the user account needs to be retained, please submit an Extend User form to change their account from temporary to permanent.<br>
    •	You can find the Delete User Account request and the Extend User request on the <a href="https://esdticketsystem.moe.govt.nz/asm/Portal.aspx?&portal=moe">Service Desk Portal</a>.<br>
    •	It is your responsibility as a manager to retrieve and return and hardware assigned to your staff member. <br>
    <br>
    If you have already submitted a request for this staff member please respond with your request number.<br>
    <br>
    If you have any further questions, please contact the Service Desk via email or call +6444638446<br>
    """


"""takes the values extracted from the ticket and writes an email in the form of a .eml file"""
def create_email(user, manager, end_date):
    manager_email = emailise(manager)
    msg            = MIMEMultipart('alternative')
    msg['Subject'] = 'Staff Resigned Email - ' + user
    msg['To']      = manager_email
    msg['From']    = 'service.desk@education.govt.nz'
    msg.add_header('X-Unsent', '1')

    html = f"""\
    <html>
        <head></head>
        <body>{email_text(user, manager.split()[0], end_date)}</body>
    </html>"""
    
    part = MIMEText(html, 'html')
    msg.attach(part)

    outfile_name = file_path + 'email_sample.eml'
    with open(outfile_name, 'w+') as outfile:
        gen = generator.Generator(outfile)
        gen.flatten(msg)
    outfile.close()


#The main execution. The programme repeatedly generates emails from given tickets until the user gives the end command 'x'
info_x, info_y = 39, 49 #magic numbers. These are the positions in a standard delete user ticket of the lines with user, manager, and date.
while 1:
    ticket = read_ticket().split("\n")
    values = extract((ticket[info_x], ticket[info_y]))
    print(values)
    create_email(*values)
    os.startfile(file_path + "email_sample.eml")
    cont = input("press x then enter to close programe, or enter to run again: ")
    if cont == "x":
        break
