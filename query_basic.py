import logging
import rdflib
from _pyio import open

# configuring logging
logging.basicConfig()

query = """
PREFIX ma: <http://www.semanticweb.org/natalia/project1#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
SELECT DISTINCT ?name ?publisher
WHERE { ?videoGame rdf:type ma:VideoGame .
        ?videoGame ma:name  ?name .
        ?videoGame ma:publisher ?publisher .
        }"""



# creating the graph
g=rdflib.Graph()
result=g.parse("new.owl", "xml")
print("graph has %s statements.\n" % len(g))


# querying and displaying the results
print ('{0:45s} {1:10s}'.format("Name","abstract"))
for x,y in g.query(query):
    print ('{0:45s} {1:10s}'.format(x,y))