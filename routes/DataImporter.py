from flask import Blueprint, jsonify
from flask import request
from persistence.graph import graph_auth
from parsers.Parser import parser_articles, parser_inproceedings, parser_incollections

route2 = Blueprint('dataimporter', __name__)
graph = graph_auth("dblpDB")


@route2.route('/parsing')
def get_publications_author():
    num_records = int(request.args.get('num_records'))
    parser_articles('files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    parser_inproceedings('files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    parser_incollections('files/dblp.xml.gz', '<!DOCTYPE dblp SYSTEM "dblp.dtd">', num_records, False)
    return jsonify({"status": 200, "message": "Data imported"})
