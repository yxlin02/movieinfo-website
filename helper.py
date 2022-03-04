from numpy import sort
from datasource import *

def getMovieListFromDB(inputDict):
    database = DataSource()
    if (inputDict):
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
                database.addYearRange(str(inputDict[key]), str(inputDict['endYear']))
            elif key == 'startScore':
                database.addScoreRange(str(inputDict[key]), str(inputDict['endScore']))
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
        newDict['startYear'] = form['startYear']
    if 'endYear' in form:
        newDict['endYear'] = form['endYear']
    if 'startScore' in form:
        newDict['startScore'] = form['startScore']
    if 'endScore' in form:
        newDict['endScore'] = form['endScore']
    if 'order' in form:
        newDict['order'] = form['order']
    if 'sort' in form:
        newDict['sort'] = form['sort']
    if 'rating' in form:
        newDict['rating'] = form['rating']
    return newDict


def getSearchInfo(inputDict):
    info = ''
    for key in inputDict:
        if key in ['Title', 'Genre', 'Country', 'Company', 'Actor', 'Writer', 'Directoor']:
            info = info + inputDict[key] + ' ' 
        elif key == 'startYear':
            info = info + '(released between ' + inputDict[key]
        elif key == 'endYear':
            info = info + ' & ' + inputDict[key]
        elif key == 'startScore':
            info = info + ' with scores between ' + inputDict[key]
        elif key == 'endScore':
            info = info + ' & ' + inputDict[key] + ')'
    return info

def addTopTenFilter(inputDict):
    newDict = inputDict
    newDict['startYear'] = newDict['endYear'] = '2020'
    newDict['sort'] = 'IMBDScore'
    newDict['order'] = 'DESC'
    newDict['limit'] = '10'
    return newDict