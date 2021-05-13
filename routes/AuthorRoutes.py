from flask import jsonify
from flask import Blueprint
from flask import request
from persistence.graph import graph_auth
from persistence.queries import query1, query2, query3, query4, query5, query6, query6_2, query8, query9, query10, \
    query11, query13, query14

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


@route1.route('/topk/query6_2')
def get_topk_authors_query6_2():
    k = int(request.args.get('k'))
    data = graph.run(query6_2, k=k).data()
    return jsonify(data)


@route1.route('/topk/query8')
def get_topk_authors_query8():
    k = int(request.args.get('k'))
    data = graph.run(query8, k=k).data()
    return jsonify(data)


@route1.route('/topk/query9')
def get_topk_authors_query9():
    k = int(request.args.get('k'))
    author_name = str(request.args.get('author_name'))
    data = graph.run(query9, name=author_name, k=k).data()
    return jsonify(data)


@route1.route('/publications/query10')
def get_query10():
    year = str(request.args.get('year'))
    data = graph.run(query10, year=year).data()
    return jsonify(data)


@route1.route('/pages/query11')
def get_query11():
    year = str(request.args.get('year'))
    author_name = str(request.args.get('author_name'))
    data = graph.run(query11, name=author_name, year=year).data()
    return jsonify(data)


@route1.route('/three_coauthors/query13')
def get_query13():
    journal_name = str(request.args.get('journal_name'))
    data = graph.run(query13, name=journal_name).data()
    return jsonify(data)


@route1.route('/query14')
def get_query14():
    data = graph.run(query14).data()
    return jsonify(data)
