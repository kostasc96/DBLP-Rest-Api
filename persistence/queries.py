query1 = """
    MATCH (n:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    WHERE n.name = $name
    RETURN p.title as title,p.year as year
    """

query2 = """
    MATCH (:Author{name:$name})-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
    WHERE p.year = $year
    RETURN $name as name,count(c) as no_coauthorships
    """
