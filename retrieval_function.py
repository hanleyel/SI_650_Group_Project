import csv
import numpy as np
import math

'''
term = 'the query term'
av_dl = 'average document length of the collection'
doc_term_count = 'number of times the term appears in the current document'
doc_size = 'total number of terms in the current document'
num_docs = 'total number of documents in the index'
doc_count = 'number of documents that a term t_id appears in'
query_term_weight = 'query term count (or weight in case of feedback)'
'''

class BM25():
    def __init__(self, k1=1.2, b=0.75, k3=500):
        self.k1 = k1
        self.b = b
        self.k3 = k3
        self.term = input('Please enter your query term: ')
        self.num_docs = 0
        self.total_dl = 0
        self.doc_count = 0
        self.query_term_weight = 1
        with open('dataset.csv') as infile:
            csv_reader = csv.reader(infile, delimiter=',')
            for row in csv_reader:
                self.num_docs += 1

                doc = row[2]
                doc_lst = doc.split()
                self.total_dl += len(doc_lst)

                self.doc_term_count = doc_lst.count(self.term)
                self.doc_count += self.doc_term_count
                self.doc_size = len(doc_lst)

        self.avg_dl = self.total_dl / self.num_docs

    def scorer(self):
        k1 = self.k1
        b = self.b
        k3 = self.k3
        doc_term_count = self.doc_term_count
        doc_size = self.doc_size
        avg_dl = self.avg_dl
        num_docs = self.num_docs
        doc_count = self.doc_count
        query_term_weight = self.query_term_weight

        tf = ((k1+1)*doc_term_count)/(k1*(1-b+b*(doc_size/avg_dl))+doc_term_count)
        print(tf)

        idf = math.log((num_docs-doc_count+0.5)/(doc_count+0.5)) # this line gives a math domain error when the query term is common
        print(idf)

        qtf = ((k3+1)*query_term_weight)/(k3+query_term_weight)

        print(np.dot(np.dot(tf, idf), qtf))

        return np.dot(np.dot(tf, idf), qtf)

ranker = BM25()

ranker.scorer()