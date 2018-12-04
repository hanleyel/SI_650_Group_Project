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
        # self.term = term

    def scorer(self, filename, term):
        k1 = self.k1
        b = self.b
        k3 = self.k3
        # term = self.term
        num_docs = 0
        total_dl = 0
        doc_count = 0
        query_term_weight = 1
        with open(filename) as infile:
            csv_reader = csv.reader(infile, delimiter=',')
            for row in csv_reader:
                # print(row)
                num_docs += 1
                doc = row[2]
                doc_lst = doc.split()
                total_dl += len(doc_lst) # Total length of doc
                doc_term_count = doc_lst.count(term) # count of term in doc
                if doc_term_count > 0:
                    doc_count += 1 # total count of term in corpus
                doc_size = len(doc_lst) # Total length of doc

        infile.close()

        avg_dl = total_dl / num_docs

        with open(filename) as infile:
            result_dict = {}
            csv_reader = csv.reader(infile, delimiter=',')
            for row in csv_reader:
                title = row[0]
                doc = row[2]
                doc_lst = doc.split()
                doc_term_count = doc_lst.count(term)

                tf = ((k1+1)*doc_term_count)/(k1*(1-b+b*(doc_size/avg_dl))+doc_term_count)
                # print(tf)

                # print("num_docs: {}\tdoc_count: {}\t e^idf:{}".format(num_docs, doc_count, ((num_docs-doc_count+0.5)/(doc_count+0.5))))
                idf = math.log(((num_docs-doc_count)+0.5)/(doc_count+0.5)) # this line gives a math domain error when the query term is common
                # print(idf)

                qtf = ((k3+1)*query_term_weight)/(k3+query_term_weight)

                score = np.dot(np.dot(tf, idf), qtf)


                # print('{},{}'.format(score, title))

                result_dict[title] = score


                # if score > 0:
                #     print(row)

            sorted_results = sorted(result_dict, key=lambda x: result_dict[x], reverse=True)
            for i in sorted_results:
                print("{}, \t{}".format(i, result_dict[i]))
                # print(score)

                result_dict[title] = score


                # if score > 0:
                    # print(row)
            #sorted_dict = sorted(result_dict)
            sorted_dict = sorted_results

        infile.close()

        results_html = ''
        for ele in sorted_dict:
            results_html += '<p>'+ele+'</p>'

        return results_html

# ranker = BM25()
#
# print(ranker.scorer('dataset.csv', term='Policing'))
