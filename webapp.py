import flask
from flask import render_template, request
import json
import sys
from datasource import *
from helper import *

app = flask.Flask(__name__)

globalInputDict = {
    'startYear': '1980',
    'endYear': '2020',
    'startScore': '1',
    'endScore': '10',
    'sort': 'releasedYear',
    'order': 'ASC'
}

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def resetGlobalVar():
    globalInputDict = {
        'startYear': '1980',
        'endYear': '2020',
        'startScore': '1',
        'endScore': '10',
        'sort': 'releasedYear',
        'order': 'ASC'
    }

def updateGlobalVar(inputDict):
    globalInputDict = inputDict

@app.route('/')
def homePage():
    resetGlobalVar()
    return render_template('index.html')

@app.route('/about')
def aboutData():
    resetGlobalVar()
    return render_template('about.html')

@app.route('/results', methods=['POST', 'GET'])
def searchResult():
    localInputDict = globalInputDict
    if request.method == 'POST':
        localInputDict = getFormInput(localInputDict, request.form)
        searchInfo = getSearchInfo(localInputDict)
        localMovieList = getMovieListFromDB(localInputDict)
        numResult = len(localMovieList)
    updateGlobalVar(localInputDict)
    return render_template('result.html', moviesList = localMovieList, searchInput = searchInfo, numOfResult = numResult, inputDict = localInputDict)    

@app.route('/top10')
def getTopTen():
    localInputDict = globalInputDict
    localInputDict = addTopTenFilter(localInputDict)
    searchInfo = getSearchInfo(localInputDict)
    localMovieList = getMovieListFromDB(localInputDict)
    numResult = len(localMovieList)
    updateGlobalVar(localInputDict)
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