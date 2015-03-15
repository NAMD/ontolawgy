# -*- coding: utf-8 -*-


import nltk
from nltk.tokenize import WordPunctTokenizer
import string
from collections import defaultdict
from nltk.stem.snowball import PortugueseStemmer

stemmer = PortugueseStemmer()
import operator
import tools
import rdflib

# todo 1: Separador de texto (se os textos vierem como um único arquivo com tudo junto); ou de alguma forma tratar um input de vários textos
# todo 2: Fazer as instanciações a cada texto colocando como propriedade a que texto pertence
# todo 3: Ativar o reasoner
# todo 4 Contar quantos objetos com as características desejadas nós temos, fazendo assim as "coordenadas" de cada texto
# todo 5: Calcular a distância entre cada texto.
# todo 6: Fazer a k-clusterização para separar os textos em categorias.

# Vou começar usando o banco de dados que tenho, no qual os textos são exportados como arquivos únicos

def use_and_prepare_text(arquivo, splitter=','):
    #abre o arquivo, retornando uma lista de textos.
    file1 = open(arquivo, 'r+')
    texto = file1.read()
    texto = texto.decode('utf-8')
    texto = texto.split(splitter)
    return texto


def instanciator(arg_main, arg_text_name, list_of_classes, class_manifestations, namespace_string):
    #arg = argument; #arg_main é lista de palavras; class_manifestations é um dicionário, com chave sendo o nome da classe, valores sendo as manifestações
    text_name = arg_text_name.replace(' ', '')
    ns = rdflib.Namespace(namespace_string)
    ontology_name = 'http://www.semanticweb.org/fgv/ontologies/2014/3/' + text_name
    file_text = '<?xml version="1.0"?>\n\n\n<!DOCTYPE rdf:RDF [\n    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >\n    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n    <!ENTITY ontologia-juridica "http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#" >\n]>\n\n\n'
    file_text = file_text + '<rdf:RDF xmlns="' + ontology_name + '#"\n     xml:base="' + ontology_name + '"\n     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n     xmlns:owl="http://www.w3.org/2002/07/owl#"\n     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n     xmlns:ontologia-juridica="http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#">\n    '
    file_text = file_text + '<owl:Ontology rdf:about='
    file_text = file_text + '"' + ontology_name + '">\n        <owl:imports rdf:resource="http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica"/>\n    </owl:Ontology>\n    \n\n\n    <!-- \n    ///////////////////////////////////////////////////////////////////////////////////////\n    //\n    // Individuals\n    //\n    ///////////////////////////////////////////////////////////////////////////////////////\n     -->\n\n    \n\n\n     '
    counter = 0  #objetivo: evitar instâncias de mesmo nome
    for palavra in arg_main:
        manifestacao = False  # A partir daqui será testado se a palavra é manifestação de alguma classe
        for classe in list_of_classes:
            for forma_de_manifestar in class_manifestations[classe]:
                if ns[palavra] == forma_de_manifestar:
                    manifestacao = True
                    break
            if manifestacao == True:
                break
        if manifestacao == False:
            break  # Se a palavra não for manifestação de nenhuma classe, passe pra próxima palavra

        class_name = classe

        instance_address = ontology_name + '#' + class_name + str(counter)
        file_text = file_text + '<!-- ' + instance_address + ' -->\n\n'
        file_text = file_text + '    <owl:NamedIndividual rdf:about="' + instance_address + '">\n        <rdf:type rdf:resource="&ontologia-juridica;' + class_name + '\n    </owl:NamedIndividual>\n\n\n'
        counter = counter + 1
    file_text = file_text + "</rdf:RDF>"
    return file_text


#def instanciator(arg_main, arg_text_name, list_of_classes, namespace_string): #arg = argument; #arg_main é lista de pares (palavra, documento)
#	text_name = arg_text_name.replace(' ', '')
#	ns = rdflib.Namespace(namespace_string)
#	ontology_name = 'http://www.semanticweb.org/fgv/ontologies/2014/3/' + text_name
#	file_text = '<?xml version="1.0"?>\n\n\n<!DOCTYPE rdf:RDF [\n    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >\n    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n    <!ENTITY ontologia-juridica "http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#" >\n]>\n\n\n'
#	file_text = file_text + '<rdf:RDF xmlns="' + ontology_name + '#"\n     xml:base="' + ontology_name + '"\n     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n     xmlns:owl="http://www.w3.org/2002/07/owl#"\n     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n     xmlns:ontologia-juridica="http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#">\n    '
#	file_text = file_text + '<owl:Ontology rdf:about='
#	file_text = file_text + '"' + ontology_name + '">\n        <owl:imports rdf:resource="http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica"/>\n    </owl:Ontology>\n    \n\n\n    <!-- \n    ///////////////////////////////////////////////////////////////////////////////////////\n    //\n    // Individuals\n    //\n    ///////////////////////////////////////////////////////////////////////////////////////\n     -->\n\n    \n\n\n     '
#	counter = 0 #objetivo: evitar instâncias de mesmo nome
#	for par in arg_main:
#		manifestacao = False
#		for classe in list_of_classes:
#			if ns[par[0]] == classe:
#				manifestacao = True
#				break
#		if manifestacao == False:
#			break

#		class_name = classe
#		documento = par[1]

#		instance_address = ontology_name + '#' + class_name + str(counter)
#		file_text = file_text + '<!-- ' + instance_address + ' -->\n\n'
#		file_text = file_text + '    <owl:NamedIndividual rdf:about="' + instance_address + '">\n        <rdf:type rdf:resource="&ontologia-juridica;' + class_name + '"/>\n        <ontologia-juridica:no_documento>' + str(documento) + '</ontologia-juridica:no_documento>\n    </owl:NamedIndividual>\n\n\n'
#		counter = counter + 1
#	file_text = file_text + "</rdf:RDF>"
#	return file_text

def prepare_class_list(ontology_name):  #ontol_name é o nome do arquivo da ontologia
    ontol = rdflib.Graph()
    ontol.parse(ontology_name)
    tipo = rdflib.RDF.type
    classe = rdflib.OWL.Class
    l = []
    for i in ontol.subjects(tipo, rdflib.OWL.Class):
        if type(i) == rdflib.term.URIRef:
            l.append(i)
    return l


def prepare_class_manifestations(ontology_name, class_list):
    ontol = rdflib.Graph()
    ontol.parse(ontology_name)
    tipo = rdflib.RDF.type
    classe = rdflib.OWL.Class
    class_manisf = {}
    for i in range(len(class_list)):
        a = ontol.value(class_list[i], manis)
        if a is not None:
            a = a.split(", ")
            for i in range(len(a)):
                if a[i] == "'self'":
                    class_name = class_list[i][len(ns):]
                    a[i] = class_name
        else:
            d[class_list[i]] = a
    return d


def prepare_multiple_texts_one_file(arquivo, instance_file_name, list_of_classes, ontol_name, namespace, splitter,
                                    stemmize=False):
    textos = use_and_prepare_text(arquivo, splitter)
    instance_file = open(instance_file_name, 'w+')
    list_of_classes = prepare_class_list(ontol_name)

    for k in range(len(textos)):
        if stemmize:
            par_palavras = [(stemmer.stem(token.lower()), "documento_" + str(k)) for token in
                            WordPunctTokenizer().tokenize(textos[k])]
        else:
            par_palavras = [(token.lower(), "documento_" + str(k)) for token in
                            WordPunctTokenizer().tokenize(textos[k])]

    instance_file.write(instanciator(palavras_par, instance_file_name, list_of_classes, namespace))
    instance_file.close()

#ordem de uso: prepare_class_list(ontol_name) -> prepare_multiple_texts_one_file
