import rdflib
import networkx as nx


def load_ontology(fname="../ontology/ontologia-juridica-v0-2-0.owl"):
    """

    :rtype : rdflib Graph
    """
    ontology = rdflib.Graph()
    ontology.parse(fname)
    return ontology


ns = rdflib.Namespace("http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#")


def in_namespace(namespace, node):
    if (node[:(len(namespace))] == namespace):
        return True
    else:
        return False


def predicate_graph(predicate, ontology, remove_namespace=True, no_BNodes=False):
    graph = nx.DiGraph()
    for tuple in ontology:
        if tuple[1] == predicate:
            if remove_namespace:
                if no_BNodes:
                    if type(tuple[0]) == rdflib.term.URIRef:
                        t0 = tuple[0][(tuple[0].find("#") + 1):]
                    else:
                        continue
                    if type(tuple[2]) == rdflib.term.URIRef:
                        t2 = tuple[2][(tuple[2].find("#") + 1):]
                    else:
                        continue
                    graph.add_edge(t0, t2)
                else:
                    if type(tuple[0]) == rdflib.term.URIRef:
                        t0 = tuple[0][(tuple[0].find("#") + 1):]
                    else:
                        t0 = tuple[0]
                    if type(tuple[2]) == rdflib.term.URIRef:
                        t2 = tuple[2][(tuple[2].find("#") + 1):]
                    else:
                        t2 = tuple[2]
                    graph.add_edge(t0, t2)
            else:
                graph.add_edge(tuple[0], tuple[2])
    return graph


def superclasses_of(alist, graph):
    # In this I suppose the list's elements are unicode strings which are classes in the ontology.
    #This function is bugged, don't use it.
    returned = {}
    for i in alist:
        if i in graph:
            returned[i] = nx.dag.descendants(graph, i)
        else:
            returned[i] = set()
    return returned


def csv_to_wordlist(csv_file, no_header=True):
    if no_header:
        csv_file.readline()
    aux_list = csv_file.readlines()
    wordlist = []
    for line in aux_list:
        wordlist.append(line.split('"')[1].decode('utf-8'))
    return wordlist


if __name__ == "__main__":
    "'ontol' is the ontology.\n'ns' is the default namespace."

