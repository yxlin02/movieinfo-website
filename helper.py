from numpy import sort
from datasource import *

def getMovieListFromDB(inputDict):
    '''
    This function will call on specific api in the backend based on user input dictionary (inputDict).

    return - a list of movie objects
    '''
    database = DataSource()
    for key in inputDict:
        if key == 'Title':
            database.addFilterTitle(inputDict[key])
        elif key == 'Genre':
            database.addFilterGenre(inputDict[key])
        elif key == 'Country':
            database.addFilterCountry(inputDict[key])
        elif key == 'Company':
            database.addFilterCompany(inputDict[key])
        elif key == 'Actor':
            database.addFilterActor(inputDict[key])
        elif key == 'Writer':
            database.addFilterWriter(inputDict[key])
        elif key == 'Director':
            database.addFilterDirector(inputDict[key])
        elif key == 'startYear':
            database.addFilterYearRange(inputDict[key], inputDict['endYear'])
        elif key == 'startScore':
            database.addFilterScoreRange(inputDict[key], inputDict['endScore'])
        elif key == 'rating' and not inputDict[key] == 'All':
            database.addFilterRating(inputDict[key])
        elif key == 'sort':
            if inputDict[key] == 'releasedYear':
                database.addSortByYear(inputDict['order'])
            else:
                database.addSortByScore(inputDict['order'])
        elif key == 'limit':
            database.addNumOfDisplayRows(inputDict['limit'])

    return database.getMoviesByFilters()

def getFormInput(inputDict, form):
    '''
    This function puts all the user input from request.form into a dictionary.

    return - user input dictionary
    '''
    newDict = inputDict
    if 'movie-title' in form:
        newDict['Title'] = form['movie-title']
    if 'filter-one-input' in form:
        newDict[form['filter-one']] = form['filter-one-input']
    if 'filter-two-input' in form:
        newDict[form['filter-two']] = form['filter-two-input']
    if 'filter-three-input' in form:
        newDict[form['filter-three']] = form['filter-three-input']
    if 'startYear' in form:
        newDict['startYear'] = int(form['startYear'])
    if 'endYear' in form:
        newDict['endYear'] = int(form['endYear'])
    if 'startScore' in form:
        newDict['startScore'] = int(form['startScore'])
    if 'endScore' in form:
        newDict['endScore'] = int(form['endScore'])
    if 'order' in form:
        newDict['order'] = form['order']
    if 'sort' in form:
        newDict['sort'] = form['sort']
    if 'rating' in form:
        newDict['rating'] = form['rating']
    return newDict


def getSearchInfo(inputDict):
    '''
    This function forms the information string based on user input dictionary.

    return - a string with search information
    '''
    info = ''
    for key in inputDict:
        if key in ['Title', 'Genre', 'Country', 'Company', 'Actor', 'Writer', 'Directoor']:
            info = info + inputDict[key] + ' ' 
        elif key == 'startYear':
            # not display default value
            if not inputDict['startYear'] == 1980 and not inputDict['endYear'] == 2020:
                info = info + 'released between ' + str(inputDict[key])
        elif key == 'endYear':
            if not inputDict['startYear'] == 1980 and not inputDict['endYear'] == 2020:
                info = info + ' & ' + str(inputDict[key])
        elif key == 'startScore':
            if not inputDict['startScore'] == 1 and inputDict['endScore'] == 10:
                info = info + ' with scores between ' + str(inputDict[key])
        elif key == 'endScore':
            if not inputDict['startScore'] == 1 and inputDict['endScore'] == 10:
                info = info + ' & ' + str(inputDict[key])
    return info

def addTopTenFilter(inputDict):
    '''
    This filter will add filters to select the top 10 movies based on IMBDscore in 2021.
    
    return - a modified user input dictionary 
    '''
    newDict = inputDict
    newDict['startYear'] = newDict['endYear'] = '2020'
    newDict['sort'] = 'IMBDScore'
    newDict['order'] = 'DESC'
    newDict['limit'] = 10
    return newDict