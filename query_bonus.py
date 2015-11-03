import logging
import rdflib
from _pyio import open

# configuring logging
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("new_full.owl", "xml")
print("graph has %s statements.\n" % len(g))


# FILTER (str(?name) = str(?name1)) line is a neat trick to combine individuals that are created
# from two sources.For example individual 1236 is actually the data from linkedmdb for the movie 
# Harry Potter and the Philosopher's Stone. 1236 includes raiting information for the movie 
# which is not available from DBpedia.
query="""
PREFIX ma: <http://www.semanticweb.org/natalia/project1#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?game ?publisher
WHERE { ?game ma:name ?name .
        ?game ma:publisher ?publisher .

        ?game1 ma:publisher ?publisher1 .
        ?game1 ma:name ?name1 .

        FILTER (str(?publisher) = str(?publisher1))
        FILTER regex(str(?publisher),"Electronic_Arts")
        }
        """

# querying and displaying the results
print ('{0:45s} {1:10s} '.format("Title","Publisher"))
for x,y in g.query(query):
    print ('{0:45s} {1:10s} '.format(x,y))
    