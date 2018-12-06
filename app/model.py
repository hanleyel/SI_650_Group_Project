import csv
import numpy as np
import math
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('english')

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

    def scorer(self, filename, search_term):
        k1 = self.k1
        b = self.b
        k3 = self.k3

        num_docs = 0
        total_dl = 0
        doc_count = 0

        result_dict = {}
        ref_dict = {}
        desc_dict = {}

        stop_words = set(stopwords.words('english'))
        tokens = pos_tag(word_tokenize(search_term.lower()))
        filtered_tokens = [i for i in tokens if not i in stop_words]

        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = []
        for word, tag in filtered_tokens:
            wntag = tag[0].lower()
            wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
            if not wntag:
                lemma = word
            else:
                lemma = lemmatizer.lemmatize(word, wntag)
            lemmatized_tokens.append(lemma)
        search_term = ' '.join(lemmatized_tokens)

        try:
            query_term_weight = 1/len(search_term.split())
        except:
            print('Please try another term!')
            return None

        for term in search_term.split():

            with open(filename) as infile:
                csv_reader = csv.reader(infile, delimiter=',')
                for row in csv_reader:
                    num_docs += 1
                    doc = row[5]
                    doc_lst = doc.split()
                    total_dl += len(doc_lst) # Total length of doc
                    doc_term_count = doc_lst.count(term) # count of term in doc
                    if doc_term_count > 0:
                        doc_count += 1 # total count of term in corpus
                    doc_size = len(doc_lst) # Total length of doc

            infile.close()

            avg_dl = total_dl / num_docs

            with open(filename) as infile:
                csv_reader = csv.reader(infile, delimiter=',')
                for row in csv_reader:
                    title = row[0]
                    ref = row[4]
                    doc = row[5]
                    doc_lst = doc.split()
                    doc_term_count = doc_lst.count(term)

                    tf = ((k1+1)*doc_term_count)/(k1*(1-b+b*(doc_size/avg_dl))+doc_term_count)
                    idf = math.log(((num_docs-doc_count)+0.5)/(doc_count+0.5))
                    qtf = ((k3+1)*query_term_weight)/(k3+query_term_weight)

                    score = np.dot(np.dot(tf, idf), qtf)

                    ref_dict[title] = ref
                    desc_dict[title] = row[2]
                    if title not in result_dict.keys():
                        result_dict[title] = score
                    else:
                        result_dict[title] += score

            infile.close()

        sorted_results = sorted(result_dict, key=lambda x: result_dict[x], reverse=True)



        results_html = ''
        count = 0
        for ele in sorted_results:
            if result_dict[ele] > 0:
                count += 1
                results_html += '<h3>'+str(count)+'. '+'<a href='+ref_dict[ele]+'>'+ele[2:-1]+'</a>'+'</h3><p>'+desc_dict[ele][2:500].replace('#', '').replace('\\n', "")+'...</p>'

        if count > 0:
            return results_html
        else:
            return '<p>No results found.</p>'

# ranker = BM25()
# print(ranker.scorer('dataset_cleaned.csv', search_term='police'))
