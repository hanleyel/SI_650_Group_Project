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
        results = ranker.scorer(filename='dataset_cleaned.csv', search_term=searchterm)
    else:
        searchterm = ''

    css_ref = '<head><link rel="stylesheet" href="../static/style.css">'
    font_ref = '<link href="https://fonts.googleapis.com/css?family=Lato|Roboto:300|Source+Sans+Pro" rel="stylesheet"></head>'
    search_bar = '<form action="/results" method="POST"><input type="text" name="searchterm"/> <br/><button type="submit" value="Search">Search</button></form>'
    header = '<h2>Returning datasets related to: <span class="keyword">' + searchterm + '</span></h2><br>'
    return css_ref + font_ref + search_bar + header + results


if __name__=="__main__":
    model.init()
    app.run(debug=True)