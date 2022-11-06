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


class JobPosting:
    def __init__(self, job_title, company, link):
        self.job_title = job_title
        self.company = company
        self.link = link


base_url = "https://www.indeed.com"
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
next_page = "/jobs?q=&l=CA&from=searchOnHP&vjk=71128f721ad9751f"
filename = 'test_output.jsonl'
outfile = open(filename, 'w')


for i in range(2):
    page = scraper.get(base_url + next_page)
    print(page.status_code)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    cards = soup.find_all("div", {"class": "job_seen_beacon"})
    for card in cards:
        link = card.find("a", {"class": "jcs-JobTitle"})['href']
        title = card.find("a", {"class": "jcs-JobTitle"}).text
        company_name = card.find("span", {"class": "companyName"}).text
        job_posting = JobPosting(title, company_name, link)
        line = json.dumps(job_posting.__dict__) + "\n"
        outfile.write(line)
    try:
        next_page = soup.find("a", {"data-testid": "pagination-page-next"})['href']
    except:
        break

outfile.close()
