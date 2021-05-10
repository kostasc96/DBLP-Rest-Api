from flask import jsonify
from flask import Blueprint
from flask import request
from persistence.graph import graph_auth

route1 = Blueprint('route1', __name__)
graph = graph_auth("dblpDB")

authors = [
    {
        "id": 1,
        "name": "Larry Page",
        "companies": [
            {
                "name": "Google"
            }
        ]
    },
    {
        "id": 2,
        "name": "Bill Gates",
        "companies": [
            {
                "name": "Microsoft"
            }
        ]
    }
]

query1 = """
    MATCH (n:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    WHERE n.name = $name
    RETURN p.title as title,p.year as year
    """

query2 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
    WHERE a.name = $name and c.name <> a.name and p.year = $year
    RETURN a.name as name,count(c) as no_coauthorships
    """


@route1.route('/publications/query1')
def get_publications_author():
    name_author = str(request.args.get('name_author'))
    data = graph.run(query1, name=name_author).data()
    return jsonify(data)


@route1.route('/coauthors/query2')
def get_coauthors():
    name_author = str(request.args.get('name_author'))
    year = str(request.args.get('year'))
    data = graph.run(query2, name=name_author, year=year).data()
    return jsonify(data)


@route1.route('/coauthors/<string:authorId>/year/<string:year>')
def get_coauthors_year(authorId, year):
    pass


@route1.route('/authors/conference-journal/<string:k>/<string:option>')
def get_authors_conference_journal(k, option):
    num = int(k)
    pass


@route1.route('/authors/single-work/<string:k>')
def get_authors_most_coauthors_per_single_work(k):
    k = int(k)
    pass


@route1.route('/authors/coauthors/<string:k>/<string:year>')
def get_authors_most_coauthors_year(k, year):
    k = int(k)
    pass


@route1.route('/authors/<string:k>')
def get_authors_most_active_years(k):
    k = int(k)
    pass
