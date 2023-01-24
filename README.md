# Job Search Engine Based on Knowledge Graph
**Contributors: Chuqiao Wang (wangchuq@usc.edu), Xinglei Liu (xingleil@usc.edu)**

![foxdemo](https://github.com/xingleiliu/DSCI558-Project/blob/main/UI_screenshot.png)

### YouTube Presentation
https://www.youtube.com/watch?v=LUHGj0-_-C0

### Table of Contents

* [Motivation](#motivation)
* [Data](#data)
* [Crawling](#crawling)
* [Ontology](#ontology)
* [Deduplication](#deduplication)
* [RDF Generation](#rdf-generation)
* [Recommendation System](#recommendation-system)
* [Summary](#summary)



## Motivation
As soon-to-be new graduates ourselves, we got our first inspiration from our job 
seeking experiences: skimming through long job descriptions only to see if the job matches 
with our skillset, extra efforts to tailor different resumes for positions in various industries, etc. 
We want to facilitate our job seeking process by building connections between jobs and 
companies and gather as much diverse information as possible to minimize the impact of the 
current hiring freeze. KG became our choice as it explicates and visualizes the relationships 
between skills, jobs, and companies, which provides a unique perspective other than traditional 
recommendation systems. 

## Data
We used two types of websites, job listing sites and business profile sites, to extract job 
details and company background, respectively. The former includes Indeed and Simplyhired
and the latter includes Crunchbase. Indeed offers both structured and unstructured data, and the 
other two only offers unstructured ones. See Table 1 in the Appendix for elaboration.

## Crawling
The biggest challenge during crawling is the anti-crawling mechanism of the websites. 
Since both Indeed and Crunchbase deploy Cloudflare Captchas which requires human clicking 
verification, we could not use Scrapy. Our first solution was to customize the request headers 
and mimic human users through Selenium, but the Captchas kept popping out after only a few 
pages were crawled. The second solution was to send requests via the ScrapeOp proxy server, 
but the scraping progress was slower than expected. We later speeded it up from a few thousand 
to ten of thousands of job posts in 2-3 hours by multi-threading.
Another challenge is the hidden search results. Both Indeed and Simplyhired only 
showcase the first 100 pages of each search. We initially attempted to apply several nested try-catch clauses and looked for HTML elements containing hyperlinks. After this attempt failed, 
we specified the range of each search, for example, location and job category. We narrowed 
down our job category to software engineers, data scientists and UI/UX designers, and 
locations to CA, TX, NY, GA, and WA, all of which carry great tech and access to 
cosmopolitan resources. At last, we successfully scraped off a total of 26980 job posts from 
Indeed and Simplyhired.


## Ontology
We have two types of entities: jobs and companies. For both entities, we used existed 
ontology from Schema.org. We hand-picked attributes that are more representative of the job
and the company. For example, qualifications for the former and keywords(related industries) 
for the latter. However, some similar attributes in the existed ontology may cause repetition in 
the future. For example, qualifications and responsibilities, baseSalary and estimatedSalary, 
etc. We dropped these similar attributes. See Table 2 and 3 in the Appendix for elaboration.
Information Extraction
We wanted to extract the missing key attributes and show them to the candidates in an 
intuitive way. Sometimes a candidate is required to fluently code in Java but the scraping 
mechanism of the website fails to capture this requirement; sometimes the salary is missing. 
Our first solution was to use spaCy NER model, but the existed model could only identify 
salary and did a bad job at identifying other properties such as qualifications: it recognized 
“Python” and “Java” as geographical locations rather than programming skills. Due to the time 
limit, we did not train our own NER model but built a customized lexicon instead. We used 
simple random sampling to select job posts to check how many percentages of entities 
(quaifications, salaries, etc.) were detected. The final percentage of entities detected over the 
samples was around 98.4%.


## Deduplication
Three properties were taken as blocking conditions: title, company, and jobLocation. 
We saw a 98.5% decrease of duplicate pairs since the first block from 52367 to 1361 pairs of 
duplicate positions. To detect false positives, we compared the job description texts and 
qualification texts of two jobs. Once their Jaccard similarity is above a certain threshold
(usually 60%), they are defined as the same post. The FPR is 6.3%.


## RDF generation
In our KG, jobs and companies are entities, and the edges are their properties. We used 
rdflib to generate RDF triples and the job posting urls as URIs for job postings since each of 
them was unique. The same applied to the company entities, except that the urls came from
Crunchbase. We stored the triples in a .ttl file.


## Recommendation System
We relied on KG Embedding models to find the nearest neighbors of each job entity, 
thus making similar job recommendations to our users when they click in one job post. There 
were three models being used: complEx, DistMult, and transE. We compared their MRR score 
and hits @1, 3 and 10. The former two models had similar hits@ values, but complEx had a 
higher MRR score. We picked complEx model as our recommendation model.

## Summary
Through this project, we got hands-on experience on how to construct a KG from 
scratch and learnt how each step of the KG construction flow works. During information 
extraction, we learnt the limits of NER models. When looking for the appropriate KG models, 
we reviewed the functions and advantages of models in lectures and had a better understanding 
when and how to use them.
