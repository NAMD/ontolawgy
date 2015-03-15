import instanciator
import rdflib

# Suponho aqui que os textos estão com enconding utf-8
def use_text_by_text(arquivo, number_of_files, splitter=';FIMDADECISAO;', ontologia='ontologia-juridica-v0-2-0.owl',
                     ns=rdflib.Namespace("http://www.semanticweb.org/fgv/ontologies/2013/8/ontologia-juridica#")):
    file1 = open(arquivo, 'r+')
    list_of_classes = prepare_class_list(ontologia)
    class_manifestations = prepare_class_manifestations(ontologia,
                                                        list_of_classes)  #falta lemmatizar as manifestações das classes
    for i in range(number_of_files):
        texto = ''
        while texto.find(splitter) == -1:
            texto = texto + file1.next().decode('utf-8')
        texto = texto[: texto.find(splitter)]
        ###função mágica que pega texto e devolve uma lista das palavras lemmatizadas: palavras = função_mágica(texto)
        nome_do_arquivo = 'instancias' + str(i) + '.owl'
        file_text = instanciator.instanciator(palavras, nome_do_arquivo, list_of_classes, ns)
        file_output = open(nome_do_arquivo, 'r+')
        file_output.write(file_text)
        file_output.close()
