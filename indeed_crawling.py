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
    def __init__(self, job_title, company, link):
        self.job_title = job_title
        self.company = company
        self.link = link


DRIVER_PATH = 'C:/Users/jenny/OneDrive/Desktop/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.indeed.com/jobs?q=&l=CA')

filename = 'indeed_postings_' + today + '.jsonl'
outfile = open(filename, 'w')
# location = driver.find_element(by=By.ID, value="text-input-where")
# location.clear()
# location.send_keys("CA")
# submit = driver.find_element(by=By.CLASS_NAME, value="yosegi-InlineWhatWhere-primaryButton")
# submit.click()
driver.implicitly_wait(3)
while True:
    job_cards = driver.find_elements(by=By.CLASS_NAME, value="job_seen_beacon")
    # print(len(job_cards))
    for job in job_cards:
        try:
            title_line = job.find_element(by=By.CLASS_NAME, value="jcs-JobTitle")
            title = title_line.find_element(by=By.CSS_SELECTOR, value="span").text
            link = title_line.get_attribute("href")
            company_name = job.find_element(by=By.CLASS_NAME, value="companyName").text
            job_posting = JobPosting(title, company_name, link)
            line = json.dumps(job_posting.__dict__) + "\n"
            outfile.write(line)

        except NoSuchElementException:
            continue

    try:
        next_page = driver.find_element(by=By.CSS_SELECTOR, value='[data-testid="pagination-page-next"]')
    except NoSuchElementException:
        break
    next_page.click()

outfile.close()



# import requests
#
# url = 'https://www.indeed.com/'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
# }

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Connection": "keep-alive",
#     "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
# }

# response = requests.get(url=url)
# print(response.text)


# from scrapfly import ScrapflyClient, ScrapeConfig
#
# client = ScrapflyClient(key='scp-live-3c569f58666e41dda01e9a03660b2f3d')
# result = client.scrape(ScrapeConfig(
#     url="https://www.indeed.com/jobs?q=python&l=Texas",
#     asp=True,
#     # ^ enable Anti Scraping Protection
# ))
# print(result.content)