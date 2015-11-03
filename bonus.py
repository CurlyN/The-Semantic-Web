import logging
import rdflib
from rdflib import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory


# configuring logging
logging.basicConfig()
 
# configuring the end-point and constructing query
# the given construct query will add the data to the existing individuals 
# it will rather add new individual movies to the graph with the data from linkedmdb
# this is not an ideal solution but works fine with the Sparql query in the query_bonus.py.
# If you open the full_example.owl in Protege you will find out that the individuals 
# 1236,1237,1238,1239 are the movie data from linkedmdb.
sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
construct_query="""
      PREFIX ma: <http://www.semanticweb.org/natalia/project1#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX games: <http://fr.dbpedia.org/property/>
      PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dc: <http://fr.dbpedia.org/property/>
      prefix owl: <http://www.w3.org/2002/07/owl#>
      
      CONSTRUCT {
      ?game rdf:type ma:VideoGame .
      ?game ma:publisher ?publisher .
      ?publisher owl:sameAs <http://fr.dbpedia.org/page/Electronic_Arts> .



      }
       WHERE{

       ?game dbpedia-owl:publisher ?publisher .
       ?publisher dbpedia-owl:wikiPageID 3778794 .



       }"""

sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef('http://www.semanticweb.org/store/movie')
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store 
g = sparql.query().convert()
g.parse("new.owl")
# the graph will be saved as full_example.owl. You can open the file with Protege to inspect it.
g.serialize("new_full.owl", "xml")
