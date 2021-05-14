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
    RETURN name,max(no_coauthors) as co_authors
    ORDER BY max(no_coauthors) DESC
    LIMIT $k
"""

query5 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(:Publication{year:$year})<-[:HAS_CONTRIBUTED]-(c:Author)
    WHERE a.name <> c.name
    RETURN a.name as name,count(c) as no_coauthors
    ORDER BY count(c) DESC
    LIMIT $k
"""

query6_2 = """
    CALL {
        MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
        RETURN a.name as name,max(toInteger(p.year)) as latest_year, min(toInteger(p.year)) as earliest_year
    }
    RETURN name, latest_year-earliest_year+1 as years_active
    ORDER BY years_active DESC
    LIMIT $k
"""

query6 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    RETURN a.name as name,count(DISTINCT p.year) as years_active
    ORDER BY years_active DESC
    LIMIT $k
"""

query8 = """
    CALL{
        MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication{category:"article"})
        RETURN a.name as name,p.year as year,count(ID(p)) as no_articles
    }
    RETURN name, round(AVG(no_articles),3) as average_per_year
    ORDER BY average_per_year DESC
    LIMIT $k
"""

query9 = """
    CALL {
        MATCH (a:Author{name:$name})-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(b:Author)-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
        WHERE NOT (a)-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(c) AND b.name <> $name AND c.name <> $name AND b.name <> c.name
        RETURN a.name as a_name,c.name as name, COUNT(DISTINCT b) as common_coauths
    }
    RETURN name,common_coauths
    ORDER BY common_coauths DESC
    LIMIT $k
"""

query9_1 = """
    MATCH (a:Author{name:$name})-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(b:Author)
    RETURN ID(b)
"""

query9_2 = """
    MATCH (b:Author)-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author)
    WHERE ID(b) in $coauthors AND c.name <> $name AND NOT (c)-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(:Author{name:$name})
    RETURN c.name as name, COUNT(DISTINCT b) as common_coauths
    ORDER BY common_coauths DESC
    LIMIT $k
"""

query10 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication{year:$year})
    WITH a.name as name,COUNT(p) as count
    WHERE count>3
    RETURN name,count
"""

query11 = """
    MATCH (:Author{name:$name})-[:HAS_CONTRIBUTED]->(p:Publication{year:$year})
    RETURN $name as name, sum(p.pagesNo) as pages_no
"""

query12 = """
    MATCH (j:Journal{name:$name})-[:HAS_ARTICLE]->(p:Publication{year:$year})<-[:HAS_CONTRIBUTED{position:$pos}]-(a:Author)
    RETURN a.name as name, COUNT(p) as count
    ORDER BY count DESC
    LIMIT $k
"""

query13 = """
    CALL {
        MATCH (j:Journal{name:$name})-[:HAS_ARTICLE]->(p:Publication)<-[:HAS_CONTRIBUTED]-(c:Author),(a:Author)-[:HAS_CONTRIBUTED]->(p)<-[:HAS_CONTRIBUTED]-(b:Author)
        RETURN a.name as coauthor_1,b.name as coauthor_2,c.name as coauthor_3, COUNT(p) as count
        ORDER BY count DESC
        LIMIT 1
    }
    RETURN coauthor_1,coauthor_2,coauthor_3
"""

query14 = """
    MATCH (b:Book)-[:HAS_PUBLICATION]->(:Publication)<-[:HAS_CONTRIBUTED]-(a:Author),(b)-[:HAS_PUBLICATION]->(:Publication)<-[:HAS_CONTRIBUTED]-(a2:Author)
    WHERE (NOT (a)-[:HAS_CONTRIBUTED]->(:Publication)<-[:HAS_CONTRIBUTED]-(a2)) AND ID(a) < ID(a2)
    RETURN a.name as author_1,a2.name as author_2
"""

query15 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    WITH DISTINCT a.name as name, p.year as year 
    WITH name, collect(toInteger(year)) as years
    WITH name, apoc.coll.sort(years) as sorted_years
    WHERE size(sorted_years) = $k
    WITH name,sorted_years,reduce(result=true, i IN range(1, size(sorted_years) - 1) |
        CASE
        WHEN sorted_years[i] = sorted_years[i-1]+1 AND result=true THEN true
        ELSE false
        END
    ) AS result
    WHERE result=true
    RETURN name
"""

query16 = """
    CALL {
        MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)<-[:HAS_CONTRIBUTED]-(b:Author)
        RETURN a.name as name, p.title, COUNT(DISTINCT b) as count_auths
    }
    RETURN name, AVG(count_auths) as average_number
    ORDER BY average_number DESC
    LIMIT $k
"""

query17 = """
    MATCH (a:Author)-[:HAS_CONTRIBUTED]->(p:Publication)
    WITH DISTINCT a.name as name, p.year as year 
    WITH name, collect(toInteger(year)) as years
    WITH name, apoc.coll.sort(years) as sorted_years
    WHERE size(sorted_years) > 1
    WITH name,sorted_years,reduce(result=false, i IN range(1, size(sorted_years) - 1) |
        CASE
        WHEN sorted_years[i] - sorted_years[i-1] >= $n OR result=true THEN true
        ELSE false
        END
    ) AS result
    WHERE result=true
    RETURN name
"""

query18 = """
    CALL {
        MATCH (b:Book)-[:HAS_PUBLICATION]->(p:Publication)<-[:HAS_CONTRIBUTED]-(a:Author)
        RETURN b.name, a.name as name, COUNT(p) as count
    }
    RETURN name, count
    ORDER BY count DESC
    LIMIT 1
"""
