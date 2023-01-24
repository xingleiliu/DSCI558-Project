from flask import Flask, jsonify, request
import requests
import re
import json
import rdflib

app = Flask(__name__)
job_kg = rdflib.Graph()
job_kg.parse('job_kg.ttl', format="turtle")
with open('data/company_info.jsonl', 'r') as input_file:
    json_list = list(input_file)


def get_job_postings(job_title, location, company, skills):
    skills_query = ""
    for s in skills:
        skills_query += f"FILTER regex(?qualifications, \"{s}\")"
    q = ("PREFIX schema: <https://schema.org/>"
         "SELECT * WHERE {"
         "?job_uri schema:jobLocation ?location;"
         "schema:title ?title;"
         "schema:hiringOrganization ?company;"
         "schema:employerOverview ?description;"
         "schema:qualifications ?qualifications;"
         "schema:baseSalary ?salary."
         f"FILTER regex(?title, \"{job_title}\")"
         f"FILTER regex(?location, \"{location}\")"
         f"FILTER regex(?company, \"{company}\")"
         f"{skills_query}"
         "}"
         )

    # "schema:responsibilities ?responsibilities;"
    # "schema:qualifications ?qualifications."

    results = job_kg.query(q)
    output = []
    for row in results:
        # print(row.job_uri)
        row_dict = {'uri': row.job_uri, 'title': row.title, 'company': row.company, 'location': row.location, 'description': row.description, 'qualifications': row.qualifications, 'salary': row.salary}
        output.append(row_dict)
    # with open('test_output.jsonl', 'r') as json_file:
    #     json_list = list(json_file)
    # for json_str in json_list:
    #     result = json.loads(json_str)
    #     output.append(result)
    print(output)
    return jsonify(output)


@app.route('/')
def main():
    return app.send_static_file('index.html')


@app.route('/process', methods=['POST'])
def process():
    # name = request.form['name']
    job_title = request.form.get('job_title')
    location = request.form.get('location')
    company = request.form.get('company')
    skills = request.form.get('skills')
    skills = skills.split(',')
    if job_title:
        return get_job_postings(job_title, location, company, skills)
    return jsonify({'error': 'Missing data!'})


@app.route('/company')
def get_company_info():
    company_name = request.args.get('company')
    for json_str in json_list:
        company = json.loads(json_str)
        if company['Company Name'] == company_name:
            return jsonify(json_str)


@app.route('/similar')
def get_similar_jobs():
    uri = request.args.get('job_uri')
    uri = uri.replace('file:///C:/Users/jenny/PycharmProjects/dsci558_project/', '')
    # print('URI: ')
    # print(uri)
    # f"FILTER regex(str(?job_uri), \"{uri}\")"
    q = ("PREFIX schema: <https://schema.org/>"
         "SELECT * WHERE {"
         "?job_uri schema:jobLocation ?location;"
         "schema:title ?title;"
         "schema:hiringOrganization ?company;"
         "schema:employerOverview ?description;"
         "schema:qualifications ?qualifications;"
         "schema:baseSalary ?salary."
         f"FILTER regex(str(?job_uri), \"{uri}\")"
         "}"
         "LIMIT 1"
         )
    results = job_kg.query(q)
    output = []
    for row in results:
        row_dict = {'uri': row.job_uri, 'title': row.title, 'company': row.company, 'location': row.location,
                    'description': row.description, 'qualifications': row.qualifications, 'salary': row.salary}
        output.append(row_dict)

    title = output[0]['title']
    q = ("PREFIX schema: <https://schema.org/>"
         "SELECT * WHERE {"
         "?job_uri schema:jobLocation ?location;"
         "schema:title ?title;"
         "schema:hiringOrganization ?company;"
         "schema:employerOverview ?description;"
         "schema:qualifications ?qualifications;"
         "schema:baseSalary ?salary."
         f"FILTER regex(?title, \"{title}\")"
         f"FILTER regex(str(?job_uri), \"indeed\")"
         "}"
         "LIMIT 6"
         )
    results = job_kg.query(q)
    output = []
    for row in results:
        row_dict = {'uri': row.job_uri, 'title': row.title, 'company': row.company, 'location': row.location,
                    'description': row.description, 'qualifications': row.qualifications, 'salary': row.salary}
        output.append(row_dict)
    # print(output)
    return jsonify(output[1:])


if __name__ == "__main__":
    # fetch_artists()
    # get_artist_info("https://api.artsy.net/api/artists/4d8b928b4eb68a1b2c0001f2")
    app.run(debug=True, port=3030)
