from threading import Condition
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notifications import send_mail, send_whatsapp_message
import os
import time
import db

URL = "http://placement.bitmesra.ac.in/"
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TIME_INTERVAL = int(os.getenv('TIME_INTERVAL'))
all_announcements = []
all_jobs = []
COUNT = 1

def login():
    email_element = browser.find_element_by_id('txtUsername')
    password_element = browser.find_element_by_id('txtPassword')
    signin_element = browser.find_element_by_id('imgSubmit')
    email_element.send_keys(EMAIL)
    password_element.send_keys(PASSWORD)
    signin_element.click()

def announcements():
    announce_button = browser.find_element_by_link_text('Announcement')
    announce_button.click()
    table = browser.find_element_by_id('tbodydetail')
    announce_elememts = table.find_elements_by_id('subject')
    latest_announcements = list(element.text for element in announce_elememts)
    new_announcements = [announcement for announcement in latest_announcements if announcement not in all_announcements]
    if len(new_announcements)!=0 and len(all_announcements)!=0:
        msg = '\n'.join(new_announcements)
        print('New Announcement:',msg)
        send_whatsapp_message('New Announcement', msg)
        send_mail('New Announcement', msg)
    all_announcements.extend(new_announcements)

def jobs():
    jobs_button = browser.find_element_by_link_text('Jobs')
    jobs_button.click()
    table = browser.find_element_by_id('Joblist')
    row_elements = table.find_elements_by_id('trlist')
    latest_jobs = []
    for element in row_elements:
        job_element = element.find_element_by_id('cname1')
        job = job_element.text
        status = element.find_element_by_id('btnstatus')
        job += ' - ' + status.get_attribute('tt')
        latest_jobs.append(job)
    new_jobs = [job for job in latest_jobs if job not in all_jobs]
    if len(new_jobs)!=0 and len(all_jobs)!=0:
        msg = '\n'.join(new_jobs)
        print('New Job:',msg)
        send_whatsapp_message('New Job', msg)
        send_mail('New Job', msg)
    all_jobs.extend(new_jobs)

if __name__ == "__main__":
    options = Options()
    options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), options=options)
    browser.implicitly_wait(10)
    while(True):
        COUNT, all_announcements, all_jobs = db.get_data()
        localtime_since_epoch = time.time()+19800
        print("{}] {}".format(COUNT,time.strftime("%I:%M:%S %p", time.gmtime(localtime_since_epoch))))
        browser.get(URL)
        login()
        announcements()
        jobs()
        COUNT+=1
        db.store_data(COUNT, all_announcements, all_jobs)
        time.sleep(TIME_INTERVAL*60)
    browser.close()