import logging
import rdflib
from rdflib.graph import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory

# configuring logging
logging.basicConfig()
 
# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
construct_query="""
      PREFIX ma: <http://www.semanticweb.org/natalia/project1#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
      PREFIX dbpprop: <http://dbpedia.org/property/>

      CONSTRUCT {
      ?videoGame rdf:type ma:VideoGame .

      ?videoGame ma:hasGameEngine ?gameEngine .
      ?gameEngine rdf:type ma:GameEngine .

      ?platform rdf:type ma:ComputingPlatform .
      ?videoGame ma:hasPlatform ?platform .
      ?gameEngine ma:hasPlatform ?platform .

      ?videoGame ma:hasGenre ?genre .
      ?genre rdf:type ma:Genre .

      ?videoGame ma:name ?name .
      ?platform ma:name ?name .

      ?videoGame ma:abstract ?abstract .
      ?platform ma:abstract ?abstract .

      ?videoGame ma:developer ?developer .
      ?platform ma:developer ?developer .

      ?videoGame ma:media ?media .
      ?videoGame ma:publisher ?publisher .

    }
       WHERE{
       ?videoGame  rdf:type dbpedia-owl:VideoGame  .
       OPTIONAL {?videoGame dbpedia-owl:gameEngine ?gameEngine}
       OPTIONAL {?videoGame dbpedia-owl:computingPlatform ?platform}
       OPTIONAL {?gameEngine dbpedia-owl:computingPlatform ?platform}
       OPTIONAL {?videoGame dbpedia-owl:genre ?genre}
       OPTIONAL {?videoGame foaf:name ?name}
       OPTIONAL {?platform foaf:name ?name}
       OPTIONAL {?videoGame dbpedia-owl:abstract ?abstract}
       OPTIONAL {?platform dbpedia-owl:abstract ?abstract}
       OPTIONAL {?videoGame dbpprop:developer ?developer}
       OPTIONAL {?platform dbpprop:developer ?developer}
       OPTIONAL {?videoGame dbpprop:media ?media}
       OPTIONAL {?videoGame dbpprop:publisher ?publisher}
       FILTER (LANG(?abstract)="en")

    }
      """

sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef("http://www.semanticweb.org/store/project1")
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store
g = sparql.query().convert()
g.parse("project.owl")
g.serialize("new.owl", "xml")
