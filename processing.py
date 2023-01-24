import cfscrape
import json
import requests
from bs4 import BeautifulSoup

# scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
base_url = "https://www.indeed.com"

# output_file = open('description.jsonl', 'w')

company_list = []
with open('indeed_postings_details_1119.jsonl', 'r') as input_file:
    json_list = list(input_file)
    for json_str in json_list:
        job = json.loads(json_str)
        company = job['company']
        company_list.append(company)

#         description = json.dumps({"description": description}) + "\n"
#         output_file.write(description)
# output_file.close()
# print(list(set(company_list)))

response = requests.get('https://www.google.com/search?q=jp+morgan+crunchbase')
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())
base_url = 'https://www.google.com/'
url = soup.find('a', href=lambda x: x and 'www.crunchbase.com/organization' in x)['href']
page = requests.get(
                url='https://proxy.scrapeops.io/v1/',
                params={
                    'api_key': '03ffa28b-89a1-4663-8449-954c7e8b04b8',
                    'url': base_url + url,
                },
            )
soup = BeautifulSoup(page.text, "html.parser")
description = soup.find('span', {'class': 'description'})
print(description)
info = soup.find_all('li', {'class': 'ng-star-inserted'})
for i in info:
    print(i.text)
print('------------------')
other_info = soup.find('ul', {'class': 'text_and_value'}).find_all('li')
for i in other_info:
    print(i.text)

industries = []
founded_date = []
operating_status = 'active'
last_funding_type = 'Grant'

        # company_name = job['company']
        # url = base_url + job['link']
        # page = scraper.get(url)  # => "<!DOCTYPE html><html><head>..."
        # print(page.status_code)

# with open('next_page.txt', 'r') as next_page_file:
#     next_page = next_page_file.read()
#     print(next_page)
