from flask import jsonify
from flask import Blueprint
from flask import request
from persistence.graph import graph_auth
from persistence.queries import query1, query2, query3, query4, query5, query6
from operator import itemgetter

route1 = Blueprint('route1', __name__)
graph = graph_auth("dblpDB")


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


@route1.route('/topk/query3')
def get_topk_authors_query3():
    category = str(request.args.get('category'))
    k = int(request.args.get('k'))
    data = graph.run(query3, category=category, k=k).data()
    return jsonify(data)


@route1.route('/topk/query4')
def get_topk_authors_query4():
    k = int(request.args.get('k'))
    data = graph.run(query4, k=k).data()
    return jsonify(data)


@route1.route('/topk/query5')
def get_topk_authors_query5():
    k = int(request.args.get('k'))
    year = str(request.args.get('year'))
    data = graph.run(query5, year=year, k=k).data()
    return jsonify(data)


@route1.route('/topk/query6')
def get_topk_authors_query6():
    k = int(request.args.get('k'))
    data = graph.run(query6, k=k).data()
    return jsonify(data)


@route1.route('/coauthors/<string:authorId>/year/<string:year>')
def get_coauthors_year(authorId, year):
    pass
