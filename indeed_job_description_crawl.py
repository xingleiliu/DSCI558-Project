import json
import requests
from bs4 import BeautifulSoup
from datetime import date
import concurrent.futures
import threading
import re


class JobPosting:
    def __init__(self, job_title, location, company, link, job_description, posting_date):
        self.job_title = job_title
        self.location = location
        self.company = company
        self.link = link
        self.job_description = job_description
        self.posting_date = posting_date


today = date.today().strftime("%m%d")
base_url = "https://www.indeed.com"
input_file = 'indeed_postings_' + today + '.jsonl'
output_file = 'indeed_postings_details_' + today + '.jsonl'
outfile = open(output_file, 'w')
lock = threading.Lock()


def crawl_page(url):
    page = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': '03ffa28b-89a1-4663-8449-954c7e8b04b8',
            'url': url,
        },
    )
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        title = soup.find("h1", {"class": "jobsearch-JobInfoHeader-title"}).text
    except AttributeError:
        return
    job_description = soup.find("div", {"class": "jobsearch-jobDescriptionText"}).text
    # print(job_description)
    company_name = soup.find("div", {"class": "jobsearch-JobInfoHeader-subtitle"}).find("div", class_="").text
    location = soup.find("div", {"class": "jobsearch-JobInfoHeader-subtitle"}).find("div", class_="",
                                                                                    recursive=False).text

    # posting_date = soup.find("p", {"class": "jobsearch-HiringInsights-entry--bullet"}).text
    posting_date = soup.find('span', string=re.compile(r"Posted")).text

    # JobComponent-description

    # try:
    #     num_candidate = soup.find("p", {"class": "jobsearch-HiringInsights-entry"}).text
    #     job_posting = JobPosting(title, location, company_name, url, job_description, num_candidate, posting_date)
    # except AttributeError:
    job_posting = JobPosting(title, location, company_name, url, job_description, posting_date)
    # print(job_posting)
    line = json.dumps(job_posting.__dict__) + "\n"
    lock.acquire()
    outfile.write(line)
    lock.release()


with open(input_file, 'r') as input_file:
    json_list = list(input_file)
    num_postings = 0
    urls = []
    for json_str in json_list:
        num_postings += 1
        job = json.loads(json_str)
        urls.append(base_url + job['link'])
    urls = list(set(urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(crawl_page, urls)
        # for x, return_value in results:
        #     outfile.write(return_value)


outfile.close()
