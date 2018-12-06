from flask import Flask, render_template, request
# from SI_650_Group_Project.app.retrieval_function import BM25
from model import BM25

app = Flask(__name__)
ranker = BM25()
# results = ranker.scorer(filename='dataset.csv', term='new')
# print(str(results))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results_page():
    if request.method == 'POST':
        searchterm = request.form['searchterm']
        results = ranker.scorer(filename='dataset.csv', search_term=searchterm)
    else:
        searchterm = ''

    header = '<h2>Returning datasets related to: ' + searchterm + '.</h2><br>'
    return header + results


if __name__=="__main__":
    model.init()
    app.run(debug=True)