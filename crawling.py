# import cfscrape
#
# scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
# page = scraper.get("http://indeed.com")  # => "<!DOCTYPE html><html><head>..."
# print(page.status_code)
# # soup = BeautifulSoup(page.content, "html.parser")
# # print(soup.prettify())

import cloudscraper
from bs4 import BeautifulSoup
import json
import requests
from datetime import date
from datetime import date
# from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests
#
# scrapeops_logger = ScrapeOpsRequests(
#     scrapeops_api_key= '03ffa28b-89a1-4663-8449-954c7e8b04b8',
#     spider_name='ScrapeOps Test Script',
#     job_name='TestJob'
#     )
#
#
# requests = scrapeops_logger.RequestsWrapper()


today = date.today().strftime("%m%d")


class JobPosting:
    def __init__(self, job_title, company, link):
        self.job_title = job_title
        self.company = company
        self.link = link


base_url = "https://www.indeed.com"
# scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
# with open('next_page.txt', 'r') as next_page_file:
#     next_page = next_page_file.read()
filename = 'indeed_postings_' + today + '.jsonl'
outfile = open(filename, 'w')
for state in ['CA', 'NY', 'WA', 'GA', 'TX']:
    for position_title in ['software+engineer', 'data+scientist', 'ux+ui+designer']:
        next_page = "/jobs?q=" + position_title + "&l=" + state + "&sc=0kf%3Aexplvl%28ENTRY_LEVEL%29%3B&fromage=14"
        num_pages = 0

        while True:
            # page = requests.get(base_url + next_page)
            # page = scraper.get(base_url + next_page)
            page = requests.get(
                url='https://proxy.scrapeops.io/v1/',
                params={
                    'api_key': '03ffa28b-89a1-4663-8449-954c7e8b04b8',
                    'url': base_url + next_page,
                },
            )
            num_pages += 1
            if page.status_code != 200:
                print("HTTP Error Code: " + str(page.status_code))
                print("Crawled {num_pages} pages".format(num_pages=num_pages))
                with open('next_page.txt', 'w') as f:
                    f.write(next_page)
            soup = BeautifulSoup(page.content, "html.parser")
            # print(soup.prettify())
            cards = soup.find_all("div", {"class": "job_seen_beacon"})
            for card in cards:
                try:
                    link = card.find("a", {"class": "jcs-JobTitle"})['href']
                    title = card.find("a", {"class": "jcs-JobTitle"}).text
                    company_name = card.find("span", {"class": "companyName"}).text
                    job_posting = JobPosting(title, company_name, link)
                    line = json.dumps(job_posting.__dict__) + "\n"
                    outfile.write(line)
                except AttributeError or TypeError:
                    continue
            try:
                next_page = soup.find("a", {"data-testid": "pagination-page-next"})['href']
            except TypeError:
                try:
                    next_page = soup.find("div", {"class": "show-omitted-jobs"}).find("a")['href']
                except AttributeError or TypeError:
                    break
        print(state + "(" + position_title + "): " + str(num_pages) + " pages")

outfile.close()
print("Crawled {num_pages} pages".format(num_pages=num_pages))
