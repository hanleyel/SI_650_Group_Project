import csv
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

infilename = 'app/dataset.csv'
outfilename = 'app/dataset_cleaned.csv'

with open(infilename, 'r') as infile:
    csv_reader = csv.reader(infile, delimiter=',')
    with open(outfilename, 'w') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        for row in csv_reader:
            doc = row[2].replace('#', '').replace('\\n', "")

            stop_words = set(stopwords.words('english'))
            tokens = pos_tag(word_tokenize(doc.lower()))
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

            lem_row = ' '.join(lemmatized_tokens)
            csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row])
            # print([row[0], row[1], row[2], row[3], row[4], lem_row])

outfile.close()
infile.close()