import csv
import email
import imaplib
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
        print('Content:')
        email_dict['content'] = ''
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
                    email_dict['content'] += body + '\n'
        else:
            content_type = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass
            if content_type == 'text/plain':
                print(body)
                email_dict['content'] = body
        emails_dict_list.append(email_dict)

    # Open a new CSV file in write mode
    with open('C://xampp//htdocs//data//data_emails.csv', mode='w', newline='') as file:

        # Define the fieldnames for the CSV
        fieldnames = ['subject', 'from_name', 'from_address', 'content']

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

    with open('C://xampp//htdocs//data//data_emails.csv', newline='') as csvfile:
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

    matches = driver.find_elements(By.TAG_NAME, value='h5')
    due_dates = list()
    for val in matches:
        if "202" in val.text:
            due_dates.append(val.text.split(",")[1].strip())

    matches = driver.find_elements(By.TAG_NAME, value='small')
    subjects = list()
    for i, val in enumerate(matches):
        print("prova ---", val.text)
        if len(val.text) > 3:
            if i % 2 == 1:
                due_dates[i-len(subjects)] += f" / {val.text}"
            else:
                subjects.append(val.text.replace("\"", ""))

    print('ASSIGNMENTS')
    h6_tags = driver.find_elements(By.TAG_NAME, value='h6')
    assignments = list(filter(lambda x: 'is due' in x.text, h6_tags))
    for i, val in enumerate(assignments):
        assignments[i] = val.text.replace(" is due", '')

    data_dicts = []
    for i in range(len(assignments)):
        ass_dict = {}
        ass_dict['due_date'] = due_dates[i]
        ass_dict['subject'] = subjects[i]
        ass_dict['assignment_title'] = assignments[i]
        ass_dict['assignment_desc'] = "TODO"
        data_dicts.append(ass_dict)
        print("\t-", subjects[i])
        print("\t-", assignments[i])
        print("\t-", due_dates[i])
        print("--------------------------------------------")


    # Open a new CSV file in write mode
    with open('C://xampp//htdocs//data//data_icorsi.csv', mode='w', newline='') as file:

        # Define the fieldnames for the CSV
        fieldnames = ['due_date', 'subject', 'assignment_title', 'assignment_desc']

        # Create a new CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row to the CSV
        writer.writeheader()
        # Write each dictionary in the list to the CSV
        for row in data_dicts:
            print(row)
            writer.writerow(row)
