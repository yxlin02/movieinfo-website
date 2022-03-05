import flask
from flask import render_template, request
import json
import sys
from datasource import *
from helper import *

app = flask.Flask(__name__)

# This is a global dictionary that keeps track of user search history.
globalInputDict = {}

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def resetGlobalInputDict():
    '''
    This function resets globalInputDict to default values, which clears user search history.
    '''
    global globalInputDict 
    globalInputDict = {
        'Title': '',
        'Genre': '',
        'Country': '',
        'Company': '',
        'Actor': '',
        'Writer': '',
        'Directoor': '',
        'startYear': 1980,
        'endYear': 2020,
        'startScore': 1,
        'endScore': 10,
        'sort': 'releasedYear',
        'order': 'ASC'
    }

def getGlobalInputDict():
    '''
    Getter method for globalInputDict.
    '''
    return globalInputDict

def updateGlobalInputDict(inputDict):
    '''
    Setter (update) method for globalInputDict.
    '''
    global globalInputDict 
    globalInputDict = inputDict

# Home Page
@app.route('/')
def homePage():
    '''
    This function renders the Home Page with template html.
    '''
    resetGlobalInputDict()
    return render_template('index.html')

# About Data Page
@app.route('/about')
def aboutData():
    '''
    This function renders the About Data Page with template html.
    '''
    resetGlobalInputDict()
    return render_template('about.html')

# Result Page
@app.route('/results', methods=['POST', 'GET'])
def searchResult():
    '''
    This function gets user input from the form and renders the result from database with html templete.

    Note: the globalInputDict will keep track of filters applied by the user, so user can add more filters (delete fitlers) based on their previous search.
    '''
    localInputDict = getGlobalInputDict()
    if request.method == 'POST':
        localInputDict = getFormInput(localInputDict, request.form)
        searchInfo = getSearchInfo(localInputDict)
        localMovieList = getMovieListFromDB(localInputDict)
        numResult = len(localMovieList)
    updateGlobalInputDict(localInputDict)
    return render_template('result.html', moviesList = localMovieList, searchInput = searchInfo, numOfResult = numResult, inputDict = localInputDict)    

# Recommandation Page
@app.route('/top10')
def getTopTen():
    '''
    This function will render the recommandation page which shows 10 movies with highest IMBD score in 2020.
    '''
    localInputDict = getGlobalInputDict()
    localInputDict = addTopTenFilter(localInputDict)
    searchInfo = getSearchInfo(localInputDict)
    localMovieList = getMovieListFromDB(localInputDict)
    numResult = len(localMovieList)
    updateGlobalInputDict(localInputDict)
    return render_template('result.html', moviesList = localMovieList, searchInput = searchInfo, numOfResult = numResult, inputDict = localInputDict) 

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