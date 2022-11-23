from flask import Flask, jsonify, request
import requests
import re
import json
import rdflib

app = Flask(__name__)
job_kg = rdflib.Graph()
job_kg.parse('job_kg.ttl', format="turtle")


def get_job_postings(job_title):
    q = ("PREFIX schema: <https://schema.org/>"
        "SELECT * WHERE {"
         "?job_uri schema:jobLocation ?location;"
         "schema:title ?title;"
         "schema:hiringOrganization ?company."
         "FILTER regex(?title, \"^Software\")"
         "}")
    results = job_kg.query(q)
    output = []
    for row in results:
        row_dict = {'uri': row.job_uri, 'title': row.title, 'company': row.company, 'location': row.location}
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
    if job_title:
        return get_job_postings(job_title=job_title)
    return jsonify({'error': 'Missing data!'})


# @app.route('/details')
# def get_artist_info():
#     token = get_authentication()
#     artist_id = request.args.get('id')
#     artists_endpoint = "https://api.artsy.net/api/artists/"
#     result = requests.get(artists_endpoint + artist_id, headers={"X-Xapp-Token": token})
#     result = result.json()
#     needed_fields = ['name', 'birthday', 'deathday', 'nationality', 'biography']
#     result = dict([(k, result[k]) for k in result if k in needed_fields])
#     return jsonify(result).


if __name__ == "__main__":
    # fetch_artists()
    # get_artist_info("https://api.artsy.net/api/artists/4d8b928b4eb68a1b2c0001f2")
    app.run(debug=True)