from flask import Blueprint, jsonify
from flask import request
from persistence.graph import graph_auth
from parsers.Parser import parser_articles, parser_inproceedings, parser_incollections

route2 = Blueprint('dataimporter', __name__)
graph = graph_auth("dblpDB")


@route2.route('/parsing')
def get_publications_author():
    num_records = int(request.args.get('num_records'))
    graph.delete_all()

    try:
        graph.schema.drop_index('Author', 'name')
        graph.schema.drop_index('Journal', 'name')
        graph.schema.drop_index('Book', 'name')
        graph.schema.drop_index('Publication', 'year')
    except:
        None
    graph.schema.create_index('Author', 'name')
    graph.schema.create_index('Journal', 'name')
    graph.schema.create_index('Book', 'name')
    graph.schema.create_index('Publication', 'year')
    parser_articles(graph, 'files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    parser_inproceedings(graph, 'files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    parser_incollections(graph, 'files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    return jsonify({"status": 200, "message": "Data imported"})
