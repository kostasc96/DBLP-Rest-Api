import gzip
from lxml import etree
from xml.etree.ElementTree import ParseError
from lxml.etree import XMLSyntaxError
import re
from py2neo import Node
from py2neo import Relationship
from persistence.graph import graph_auth

parser = etree.XMLParser(load_dtd=True)

dtd = '<!DOCTYPE dblp SYSTEM "dblp.dtd">'

graph = graph_auth("dblpDB")
graph.delete_all()

try:
    graph.schema.drop_index('Author', 'name')
    graph.schema.drop_index('Journal', 'name')
    graph.schema.drop_index('Book', 'name')
except:
    None
graph.schema.create_index('Author', 'name')
graph.schema.create_index('Journal', 'name')
graph.schema.create_index('Book', 'name')


def parser_articles(file_name, dtd1, num1, parseAll):
    i = 0
    writing = False
    start = "<article"
    end = "</article>"
    regexp1 = "</article><[^A-Z]+"
    pattern1 = "[0-9]+-"
    pattern2 = "-[0-9]+"
    dtd = dtd1
    xml = dtd
    with gzip.open(file_name, 'rt') as f:
        for line in f:
            try:
                if i > num1 and parseAll == False:
                    break
                # print(str(i) + ": " + line)
                if end in line:
                    index = line.find(end) + len(end)
                    xml += line[:index]
                    try:
                        xmldoc = etree.fromstring(xml, parser=parser)
                    except:
                        xml = dtd
                        writing = False
                        if start in line:
                            writing = True
                            index = line.find(start)
                            xml += line[index:]
                        continue
                    title = xmldoc.find(".//title").text
                    year = xmldoc.find(".//year").text
                    journal = xmldoc.find(".//journal").text
                    pages = ""
                    pageFrom = ""
                    pageTo = ""
                    numOfPages = 1
                    if re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)):
                        pages = re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)).group(0).replace('<pages>',
                                                                                                         '').replace(
                            '</pages>', '')
                        pages = re.search("[0-9]+-[0-9]+", pages).group(0)
                        pageFrom = re.search(pattern1, pages).group(0).replace('-', '')
                        pageTo = re.search(pattern2, pages).group(0).replace('-', '')
                        numOfPages = int(float(pageTo)) - int(float(pageFrom)) + 1
                    authors = []
                    hasAuthors = False
                    if title:
                        for author in xmldoc.findall(".//author"):
                            hasAuthors = True
                            authors.append(Node("Author", name=author.text))
                    if (title == None or year == None or journal == None or hasAuthors == False):
                        if start in line:
                            writing = True
                            index = line.find(start)
                            xml += line[index:]
                        continue
                    journalNode = Node("Journal", name=journal)
                    journalNode.__primarylabel__ = "Journal"
                    journalNode.__primarykey__ = "name"
                    graph.merge(journalNode)
                    articleNode = Node("Publication", title=title, year=year, pagesNo=numOfPages, category="article")
                    graph.create(articleNode)
                    for auth in authors:
                        auth.__primarylabel__ = "Author"
                        auth.__primarykey__ = "name"
                        auth_node = graph.merge(auth)
                        if auth_node != None:
                            graph.create(Relationship(auth_node, "HAS_CONTRIBUTED", articleNode))
                        else:
                            graph.create(Relationship(auth, "HAS_CONTRIBUTED", articleNode))
                    graph.create(Relationship(journalNode, "HAS_ARTICLE", articleNode))
                    i += 1
                    # print(str(i) + " \n" + "title:" + title + " \n" + "year:" + year + " \n" + "journal:" +journal + "\n" + "numOfPages:" + str(numOfPages))
                    # for author in authors:
                    #     print(author)
                    print("Article " + str(i) + " --------------------------------")
                    xml = dtd
                    writing = False

                if start in line:
                    writing = True
                    index = line.find(start)
                    xml += line[index:]
                elif writing:
                    xml += line
            except ParseError:
                xml = dtd
                continue


def parser_inproceedings(file_name, dtd1, num1, parseAll):
    i = 0
    writing = False
    start2 = "<inproceedings"
    end2 = "</inproceedings>"
    regexp2 = "</inproceedings><[^A-Z]+"
    pattern1 = "[0-9]+-"
    pattern2 = "-[0-9]+"
    dtd = dtd1
    xml = dtd
    with gzip.open(file_name, 'rt') as f:
        for line in f:
            try:
                if i > num1 and parseAll == False:
                    break
                # print(str(i) + ": " + line)
                if end2 in line:
                    index2 = line.find(end2) + len(end2)
                    xml += line[:index2]
                    try:
                        xmldoc = etree.fromstring(xml, parser=parser)
                    except XMLSyntaxError:
                        xml = dtd
                        writing = False
                        if start2 in line:
                            writing = True
                            index2 = line.find(start2)
                            xml += line[index2:]
                        continue
                    title = xmldoc.find(".//title").text
                    year = xmldoc.find(".//year").text
                    booktitle = xmldoc.find(".//booktitle").text
                    pages = ""
                    pageFrom = ""
                    pageTo = ""
                    numOfPages = 1
                    if re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)):
                        pages = re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)).group(0).replace('<pages>',
                                                                                                         '').replace(
                            '</pages>', '')
                        pages = re.search("[0-9]+-[0-9]+", pages).group(0)
                        pageFrom = re.search(pattern1, pages).group(0).replace('-', '')
                        pageTo = re.search(pattern2, pages).group(0).replace('-', '')
                        numOfPages = int(float(pageTo)) - int(float(pageFrom)) + 1
                    authors = []
                    hasAuthors = False
                    if title:
                        for author in xmldoc.findall(".//author"):
                            hasAuthors = True
                            authors.append(Node("Author", name=author.text))
                    if (title == None or year == None or booktitle == None or hasAuthors == False):
                        if start2 in line:
                            writing = True
                            index2 = line.find(start2)
                            xml += line[index2:]
                        continue
                    bookNode = Node("Book", name=booktitle)
                    bookNode.__primarylabel__ = "Book"
                    bookNode.__primarykey__ = "name"
                    graph.merge(bookNode)
                    inproceedingNode = Node("Publication", title=title, year=year, pagesNo=numOfPages,
                                            category="inproceeding")
                    graph.create(inproceedingNode)
                    for auth in authors:
                        auth.__primarylabel__ = "Author"
                        auth.__primarykey__ = "name"
                        auth_node = graph.merge(auth)
                        if auth_node != None:
                            graph.create(Relationship(auth_node, "HAS_CONTRIBUTED", inproceedingNode))
                        else:
                            graph.create(Relationship(auth, "HAS_CONTRIBUTED", inproceedingNode))
                    graph.create(Relationship(bookNode, "HAS_PUBLICATION", inproceedingNode))
                    i += 1
                    print("Inproceeding " + str(i) + " --------------------------------")
                    # print(str(i) + " \n" + "title:" + title + " \n" + "year:" + year + " \n" + "booktitle:" +booktitle + "\n" + "numOfPages:" + str(numOfPages))
                    # for author in authors:
                    #     print(author)
                    xml = dtd
                    writing = False

                if start2 in line:
                    writing = True
                    index2 = line.find(start2)
                    xml += line[index2:]
                elif writing:
                    xml += line
            except ParseError:
                xml = dtd
                continue


def parser_incollections(file_name, dtd1, num1, parseAll):
    i = 0
    writing = False
    start3 = "<incollection"
    end3 = "</incollection>"
    regexp3 = "</incollection><[^A-Z]+"
    pattern1 = "[0-9]+-"
    pattern2 = "-[0-9]+"
    dtd = dtd1
    xml = dtd
    with gzip.open(file_name, 'rt') as f:
        for line in f:
            try:
                if i > num1 and parseAll == False:
                    break
                # print(str(i) + ": " + line)
                if end3 in line:
                    index3 = line.find(end3) + len(end3)
                    xml += line[:index3]
                    try:
                        xmldoc = etree.fromstring(xml, parser=parser)
                    except XMLSyntaxError:
                        xml = dtd
                        writing = False
                        if start3 in line:
                            writing = True
                            index3 = line.find(start3)
                            xml += line[index3:]
                        continue
                    title = xmldoc.find(".//title").text
                    year = xmldoc.find(".//year").text
                    booktitle = xmldoc.find(".//booktitle").text
                    pages = ""
                    pageFrom = ""
                    pageTo = ""
                    numOfPages = 1
                    if re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)):
                        pages = re.search("<pages>.*[0-9]+-[0-9]+.*</pages>", str(xml)).group(0).replace('<pages>',
                                                                                                         '').replace(
                            '</pages>', '')
                        pages = re.search("[0-9]+-[0-9]+", pages).group(0)
                        pageFrom = re.search(pattern1, pages).group(0).replace('-', '')
                        pageTo = re.search(pattern2, pages).group(0).replace('-', '')
                        numOfPages = int(float(pageTo)) - int(float(pageFrom)) + 1
                    authors = []
                    hasAuthors = False
                    if title:
                        for author in xmldoc.findall(".//author"):
                            hasAuthors = True
                            authors.append(Node("Author", name=author.text))
                    if (title == None or year == None or booktitle == None or hasAuthors == False):
                        if start3 in line:
                            writing = True
                            index3 = line.find(start3)
                            xml += line[index3:]
                        continue
                    bookNode = Node("Book", name=booktitle)
                    bookNode.__primarylabel__ = "Book"
                    bookNode.__primarykey__ = "name"
                    graph.merge(bookNode)
                    incollectionNode = Node("Publication", title=title, year=year, pagesNo=numOfPages,
                                            category="incollection")
                    graph.create(incollectionNode)
                    for auth in authors:
                        auth.__primarylabel__ = "Author"
                        auth.__primarykey__ = "name"
                        auth_node = graph.merge(auth)
                        if auth_node != None:
                            graph.create(Relationship(auth_node, "HAS_CONTRIBUTED", incollectionNode))
                        else:
                            graph.create(Relationship(auth, "HAS_CONTRIBUTED", incollectionNode))
                    graph.create(Relationship(bookNode, "HAS_PUBLICATION", incollectionNode))
                    i += 1
                    print("Incollection " + str(i) + " --------------------------------")
                    # print(str(i) + " \n" + "title:" + title + " \n" + "year:" + year + " \n" + "booktitle:" +booktitle + "\n" + "numOfPages:" + str(numOfPages))
                    # for author in authors:
                    #     print(author)
                    xml = dtd
                    writing = False

                if start3 in line:
                    writing = True
                    index3 = line.find(start3)
                    xml += line[index3:]
                elif writing:
                    xml += line
            except ParseError:
                xml = dtd
                continue
