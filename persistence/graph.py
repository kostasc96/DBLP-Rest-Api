from py2neo import Graph


def graph_auth(password):
    return Graph(password=password)
