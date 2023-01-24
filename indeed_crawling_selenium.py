from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date

today = date.today().strftime("%m%d")


class JobPosting:
    def __init__(self, job_title, company, link, job_description):
        self.job_title = job_title
        self.company = company
        self.link = link
        self.job_description = job_description


DRIVER_PATH = 'C:/Users/jenny/OneDrive/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.indeed.com/jobs?q=&l=CA&sc=0kf%3Aexplvl%28ENTRY_LEVEL%29%3B&fromage=7')

filename = 'indeed_postings_' + today + '.jsonl'
outfile = open(filename, 'w')
# location = driver.find_element(by=By.ID, value="text-input-where")
# location.clear()
# location.send_keys("CA")
# submit = driver.find_element(by=By.CLASS_NAME, value="yosegi-InlineWhatWhere-primaryButton")
# submit.click()
page_count = 0
while True:
    driver.implicitly_wait(3)
    job_cards = driver.find_elements(by=By.CLASS_NAME, value="job_seen_beacon")
    for job in job_cards:
        try:
            job.click()
            details = driver.find_element(by=By.CLASS_NAME, value="jobsearch-JobComponent")
            title = details.find_element(by=By.CLASS_NAME, value="jobsearch-JobInfoHeader-title").text.split('\n')[0]
            company_name = job.find_element(by=By.CLASS_NAME, value="companyName").text
            # jobsearch-JobComponent-embeddedBody
            # jobDescriptionText
            job_description = details.find_element(by=By.CLASS_NAME, value="jobsearch-JobComponent-embeddedBody").text
        except NoSuchElementException:
            continue
        try:
            link = details.find_element(by=By.ID, value="applyButtonLinkContainer").find_element(by=By.CSS_SELECTOR, value="a").get_attribute("href")
        except NoSuchElementException:
            link = job.find_element(by=By.CLASS_NAME, value="jcs-JobTitle").get_attribute("href")

        job_posting = JobPosting(title, company_name, link, job_description)
        line = json.dumps(job_posting.__dict__) + "\n"
        outfile.write(line)

    try:
        next_page = driver.find_element(by=By.CSS_SELECTOR, value='[data-testid="pagination-page-next"]')
    except NoSuchElementException:
        break
    page_count += 1
    if page_count % 10 == 0:
        print("Crawling page {num_pages}".format(num_pages=page_count))
    next_page.click()

print("Crawled {num_pages} pages".format(num_pages=page_count))
outfile.close()
