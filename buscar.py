from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from flask import Flask, render_template, request

app = Flask(__name__)

sparql = SPARQLWrapper("http://localhost:7200/repositories/Articulo")

def __init__(self, query):
    self.query = query

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/Consulta', methods=['POST'])
def buscar():
    if request.method == 'POST':
        Seleccion = request.form['Seleccion']
        if "Buscar" in request.form :
            textoBuscar = request.form['textoBuscar']
            print(textoBuscar)
            if Seleccion == "Año":
                sparql.setQuery("""
                PREFIX data: <http://data.odw.tw/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX bibo: <http://purl.org/ontology/bibo/>
                PREFIX opus: <http://lsdis.cs.uga.edu/projects/semdis/opus#>
                PREFIX rss: <http://purl.org/rss/1.0/>
                PREFIX schema: <http://schema.org/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX whois: <http://www.kanzaki.com/ns/whois#>
                SELECT ?document ?title ?year ?keywords ?doi ?link
                 WHERE {
                    ?document a bibo:AcademicArticle, schema:\%20ScholaryArticle .
                    ?document dcterms:title ?title .
                    ?document bibo:\%20doi ?doi .
                    ?document opus:year ?year .
                    ?document vivo:freetextKeyword ?keywords .
                    ?document rss:link ?link .
                     FILTER(CONTAINS(STR(?year), '""" + textoBuscar + """'))

                }
            """)
            if Seleccion == "Keywords":
                sparql.setQuery("""
                PREFIX data: <http://data.odw.tw/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX bibo: <http://purl.org/ontology/bibo/>
                PREFIX opus: <http://lsdis.cs.uga.edu/projects/semdis/opus#>
                PREFIX rss: <http://purl.org/rss/1.0/>
                PREFIX schema: <http://schema.org/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX whois: <http://www.kanzaki.com/ns/whois#>
                SELECT ?document ?title ?year ?keywords ?doi ?link
        WHERE {
            ?document a bibo:AcademicArticle, schema:\%20ScholaryArticle .
            ?document dcterms:title ?title .
            ?document bibo:\%20doi ?doi .
            ?document opus:year ?year .
            ?document vivo:freetextKeyword ?keywords .
            ?document rss:link ?link .
            FILTER(REGEX(STR(?title), '""" + textoBuscar + """', 'i'))
        }
            """)
            if Seleccion == "DOI":
                sparql.setQuery("""
                PREFIX data: <http://data.odw.tw/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX bibo: <http://purl.org/ontology/bibo/>
                PREFIX opus: <http://lsdis.cs.uga.edu/projects/semdis/opus#>
                PREFIX rss: <http://purl.org/rss/1.0/>
                PREFIX schema: <http://schema.org/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX whois: <http://www.kanzaki.com/ns/whois#>
                SELECT ?document ?title ?year ?keywords ?doi ?link
                WHERE {
                
                ?document a bibo:AcademicArticle, schema:\%20ScholaryArticle .
                ?document dcterms:title ?title .
                ?document bibo:\%20doi ?doi .
                ?document opus:year ?year .
                ?document vivo:freetextKeyword ?keywords .
                ?document rss:link ?link .
                FILTER(REGEX(STR(?doi), '""" + textoBuscar + """', 'i'))
                }
            """)
                
            sparql.setReturnFormat(JSON)
            qres = sparql.query().convert()
            
            #print('\nRESULTADOS ENCONTRADOS:\n')
            if qres:
                return render_template('Resultados.html', resultsQuery =qres)
            

@app.route('/Datos', methods=['POST'])
def Presentar():
    if request.method == 'POST':
        if "Presentar" in request.form :
            #Colocar la consulta e ir a Presentar.html para arreglar la vista en los <td> {{ results['NOMBREEEEEEEEEEEEEE']['value'] }}</td>
            sparql.setQuery("""
                BASE <http://example.com/base/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>


                SELECT (COUNT(?document) AS ?cantidad) ?nombre
                WHERE {
                    ?document a foaf:person .
                    ?document foaf:name ?nombre .
                }
                
                GROUP BY ?nombre
                ORDER BY DESC(?cantidad)
                LIMIT 10
            """)
            sparql.setReturnFormat(JSON)
            qres = sparql.query().convert()
            
            #print('\nRESULTADOS ENCONTRADOS:\n')
            if qres:
                return render_template('Presentar.html', resultsQuery =qres)

app.run(host='localhost', port=5000, debug=True)
