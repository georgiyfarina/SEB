import csv
import email
import imaplib
import urllib
from datetime import datetime
from email.utils import parseaddr
from nntplib import decode_header
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time



def get_mails(email_address: str, password: str, n_emails: int, unseen: bool = False):
    imap_server = 'imap.ti-edu.ch'

    # Connect to the IMAP server and login
    imap_connection = imaplib.IMAP4_SSL(imap_server)
    imap_connection.login(email_address, password)


    # Select the inbox and search for unseen messages
    imap_connection.select('INBOX')
    emails_kind = 'UNSEEN' if unseen else 'ALL'
    typ, data = imap_connection.search(None, emails_kind)
    msg_ids = reversed(data[0].split()[-n_emails:])

    emails_dict_list = list()
    # Fetch the messages and print their subject lines
    for msg_id in msg_ids:
        email_dict = {}
        print("#"*50)
        typ, data = imap_connection.fetch(msg_id, '(RFC822)')
        raw_msg = data[0][1]
        msg = email.message_from_bytes(raw_msg)
        subject = decode_header(msg['Subject'])
        email_dict['subject'] = subject
        print(f'Subject: {subject}')
        from_name, from_address = parseaddr(msg['From'])
        email_dict['from_name'], email_dict['from_address'] = from_name, from_address
        print(f'From: {from_name} ({from_address})')

        date_str = msg['Date']
        date_obj = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(date_str)))
        email_dict['date'] = date_obj.strftime('%d.%m.%Y %H:%M:%S')
        print(f'Date: {date_obj}')

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    print(body)
        else:
            content_type = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass
            if content_type == 'text/plain':
                print(body)
        emails_dict_list.append(email_dict)
    # Open a new CSV file in write mode
    with open('data//data_emails.csv', mode='w', newline='') as file:

        # Define the fieldnames for the CSV
        fieldnames = ['subject', 'from_name', 'from_address', 'date']

        # Create a new CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row to the CSV
        writer.writeheader()
        # Write each dictionary in the list to the CSV
        for row in emails_dict_list:
            print(row)
            writer.writerow(row)
    # Disconnect from the SMTP and IMAP servers
    imap_connection.logout()

    with open('data//data_emails.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


def get_assignments(email_address, password):
    PATH = "C://Users//georg//Documents//chromedriver.exe"
    serv = Service(PATH)
    driver = webdriver.Chrome(service=serv)

    driver.get("https://www.icorsi.ch/login/index.php")

    search = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/a')
    search.click()

    search = driver.find_element(By.ID, value='username')
    search.send_keys(email_address)

    search = driver.find_element(By.ID, value='password')
    search.send_keys(password)

    search = driver.find_element(By.TAG_NAME, value='button')
    search.click()
    time.sleep(5)

    div_assignments = driver.find_element(By.XPATH, value="/html/body/div[2]/div[3]/div/div[2]/div/section[2]")
    a_tags = div_assignments.find_elements(By.TAG_NAME, value='a')
    assignments = list()
    for link in a_tags:
        aria_label = link.get_attribute('aria-label')
        if aria_label is not None:
            label_splitted = aria_label.split(' is due activity in ')
            if len(label_splitted) >= 2:

                assignment_title, rest = label_splitted[0], label_splitted[1]
                subject = rest.split(' is due on ')[0].replace("\"", "").replace(u"\xa0", u' ')
                due_date = rest.split(' is due on ')[1]
                item = {
                    'due_date': due_date,
                    'subject': subject,
                    'assignment_title': assignment_title,
                    'assignment_desc': 'TODO'
                }
                assignments.append(item)
                print("\t-", assignment_title)
                print("\t-", subject)
                print("\t-", due_date)
                print("--------------------------------------------")
    # Open a new CSV file in write mode
    with open('data//data_icorsi.csv', mode='w', newline='') as file:

        # Define the fieldnames for the CSV
        fieldnames = ['due_date', 'subject', 'assignment_title', 'assignment_desc']

        # Create a new CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row to the CSV
        writer.writeheader()
        # Write each dictionary in the list to the CSV
        for row in assignments:
            print(row)
            writer.writerow(row)