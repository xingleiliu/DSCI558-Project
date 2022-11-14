import json
import requests
from bs4 import BeautifulSoup
from datetime import date


class JobPosting:
    def __init__(self, job_title, company, link, job_description, num_candidate, posting_date):
        self.job_title = job_title
        self.company = company
        self.link = link
        self.job_description = job_description
        self.num_candidate = num_candidate
        self.posting_date = posting_date


today = date.today().strftime("%m%d")
base_url = "https://www.indeed.com"
filename = 'indeed_postings_details_' + today + '.jsonl'
outfile = open(filename, 'w')

with open('indeed_postings_1113.jsonl', 'r') as input_file:
    json_list = list(input_file)
    for json_str in json_list:
        job = json.loads(json_str)
        company_name = job['company']
        url = base_url + job['link']
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
            continue
        # JobComponent-description
        job_description = soup.find("div", {"class": "jobsearch-jobDescriptionText"}).text
        posting_date = soup.find("p", {"class": "jobsearch-HiringInsights-entry--bullet"}).text
        try:
            num_candidate = soup.find("p", {"class": "jobsearch-HiringInsights-entry"}).text
            job_posting = JobPosting(title, company_name, url, job_description, num_candidate, posting_date)
        except AttributeError:
            job_posting = JobPosting(title, company_name, url, job_description, None, posting_date)
        line = json.dumps(job_posting.__dict__) + "\n"
        outfile.write(line)

outfile.close()
