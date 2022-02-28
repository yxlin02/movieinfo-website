import flask
from flask import render_template, request
import json
import sys
from datasource import *

app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/about')
def aboutData():
    return render_template('about.html')

@app.route('/results', methods=['POST', 'GET'])
def searchResult():
    if request.method == 'POST':
        titleSearched = request.form['movie-title']
        filterOne = request.form['filter-one']
        filterTwo = request.form['filter-two']
        filterThree = request.form['filter-three']
        filterOneValue = request.form['filter-one-input']
        filterTwoValue = request.form['filter-two-input']
        filterThreeValue = request.form['filter-three-input']
        database = DataSource()
        searchInfo = ""
        if (titleSearched):
            database.setFilterTitle(titleSearched)
            searchInfo += titleSearched + " "
        if  (filterOneValue):
            switchFilter(database, filterOne, filterOneValue)
            searchInfo += filterOneValue + " "
        if  (filterTwoValue):
            switchFilter(database, filterTwo, filterTwoValue)
            searchInfo += filterTwoValue + " "
        if  (filterThreeValue):
            switchFilter(database, filterThree, filterThreeValue)
            searchInfo += filterThreeValue
        movieList = database.getMoviesByFilters()
        numResult = len(movieList)
    
    return render_template('result.html', moviesList = movieList, searchInput = searchInfo, numOfResult = numResult)    
 
def switchFilter (DDB, filter, value):
    if filter == "Genre":
        DDB.setFilterGenre(value)
    elif filter == "Country":
        DDB.setFilterCountry(value)
    elif filter == "Company":
        DDB.setFilterCompany(value)
    elif filter == "Actor":
        DDB.setFilterActor(value)
    elif filter == "Writer":
        DDB.setFilterWriter(value)
    elif filter == "Director":
        DDB.setFilterDirector(value)
'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
