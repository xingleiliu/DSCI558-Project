from flask import Flask, jsonify, request
import requests
import re
import json
import rdflib

app = Flask(__name__)
job_kg = rdflib.Graph()
job_kg.parse('job_kg.ttl', format="turtle")
with open('company_info.jsonl', 'r') as input_file:
    json_list = list(input_file)


def get_job_postings(job_title, location, company, skills):
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
         f"FILTER regex(?qualifications, \"{skills}\")"
         "}"
         )

    # "schema:responsibilities ?responsibilities;"
    # "schema:qualifications ?qualifications."

    results = job_kg.query(q)
    output = []
    for row in results:
        row_dict = {'uri': row.job_uri, 'title': row.title, 'company': row.company, 'location': row.location, 'description': row.description, 'qualifications': row.qualifications, 'salary': row.salary}
        output.append(row_dict)
    # with open('test_output.jsonl', 'r') as json_file:
    #     json_list = list(json_file)
    # for json_str in json_list:
    #     result = json.loads(json_str)
    #     output.append(result)
    return jsonify(output)


@app.route('/')
def main():
    return app.send_static_file('index.html')


@app.route('/process', methods=['GET'])
def process():
    # name = request.form['name']
    job_title = request.args.get('job_title')
    location = request.args.get('location')
    company = request.args.get('company')
    skills = request.args.get('skills')
    print(skills)
    skills = "Python"
    if job_title:
        return get_job_postings(job_title, location, company, skills)
    return jsonify({'error': 'Missing data!'})


@app.route('/company')
def get_artist_info():
    company_name = request.args.get('company')
    for json_str in json_list:
        company = json.loads(json_str)
        if company['Company Name'] == company_name:
            return jsonify(json_str)


if __name__ == "__main__":
    # fetch_artists()
    # get_artist_info("https://api.artsy.net/api/artists/4d8b928b4eb68a1b2c0001f2")
    app.run(debug=True)
