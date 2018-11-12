import csv

'''
term = 'the query term'
av_dl = 'average document length of the collection'
doc_term_count = 'number of times the term appears in the current document'
doc_size = 'total number of terms in the current document'
num_docs = 'total number of documents in the index'
doc_count = 'number of documents that a term t_id appears in'
query_term_weight = 'query term count (or weight in case of feedback)'
'''

term = input('Please enter your query term: ')

with open('dataset.csv') as infile:
    csv_reader = csv.reader(infile, delimiter=',')
    for row in csv_reader:
        doc = row[2]
        


