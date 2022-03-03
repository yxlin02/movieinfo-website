from datasource import *

def getMovieListFromDB(inputDict):
    database = DataSource()
    if (inputDict):
        for key in inputDict:
            if key == "Title":
                database.setFilterTitle(inputDict[key])
            elif key == "Genre":
                database.setFilterGenre(inputDict[key])
            elif key == "Country":
                database.setFilterCountry(inputDict[key])
            elif key == "Company":
                database.setFilterCompany(inputDict[key])
            elif key == "Actor":
                database.setFilterActor(inputDict[key])
            elif key == "Writer":
                database.setFilterWriter(inputDict[key])
            elif key == "Director":
                database.setFilterDirector(inputDict[key])
            elif key == "startYear":
                database.setYearRange(str(inputDict[key]), str(inputDict["endYear"]))
            elif key == "startScore":
                database.setScoreRange(str(inputDict[key]), str(inputDict["endScore"]))
            elif key == "rating":
                database.setFilterRating(inputDict[key])
            elif key == "sort":
                if inputDict[key] == 'releasedYear':
                    database.setSortByYear(inputDict['order'])
                else:
                    database.setSortByScore(inputDict['order'])
    return database.getMoviesByFilters()

def getFormInput(inputDict, form):
    newDict = inputDict
    if (form['movie-title']):
        newDict["Title"] = form['movie-title']
    if (form['filter-one-input']):
        newDict[form['filter-one']] = form['filter-one-input']
    if (form['filter-two-input']):
        newDict[form['filter-two']] = form['filter-two-input']
    if (form['filter-three-input']):
        newDict[form['filter-three']] = form['filter-three-input']
    return newDict


def getSearchInfo(inputDict):
    info = ""
    if (inputDict):
        for key in inputDict:
            info = info + inputDict[key] + " " 
    return info


def addFiltersToInputDict(inputDict, form):
    newDict = inputDict
    newDict['startYear'] = form['startYear']
    newDict['endYear'] = form['endYear']
    newDict['startScore'] = form['startScore']
    newDict['endScore'] = form['endScore']
    if (form['order']):
        newDict['order'] = form['order']
    if (form['sort']):
        newDict['sort'] = form['sort']
    if form['rating'] == 'All':
        if 'rating' in newDict:
            newDict.pop('rating')
    else:
        newDict['rating'] = form['rating']
    return newDict

# def getSortInput(form):
#     sortDict = {}


# def sortMovieList(sortDict, movieList):
