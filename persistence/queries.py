query1 = """
    MATCH (n:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    WHERE n.name = $name
    RETURN p.title as title,p.year as year
    """

query2 = """
    MATCH (:Author{name:$name})-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
    WHERE $name <> c.name and p.year = $year
    RETURN DISTINCT c.name as name,count(p) as no_coauthorships
    """

query3 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication{category:$category})
    RETURN DISTINCT a.name,count(p) as count
    ORDER BY count(p) DESC
    LIMIT $k
    """

query4 = """
    CALL {
        MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
        WHERE a.name <> c.name
        RETURN a.name as name,p.title as title,count(c) as no_coauthors
    }
    RETURN DISTINCT name,no_coauthors
    ORDER BY no_coauthors DESC
    LIMIT $k
"""
