import psycopg2
import psqlConfig as config
class Movie:
    def __init__(self, movieInfo):
        self.title = movieInfo[0]
        self.rating = movieInfo[1]
        self.genre = movieInfo[2]
        self.year = movieInfo[3]
        self.score = movieInfo[4]
        self.director = movieInfo[5]
        self.writer = movieInfo[6]
        self.star = movieInfo[7]
        self.country = movieInfo[8]
        self.runtime = movieInfo[9]
class DataSource:
    '''
    DataSource executes all of the queries on the database. It executes by editing the PSQL query string through setter methods.
    It also formats the data to send back to the frontend, in a list of Movie objects.
    '''
    

    def __init__(self):
        '''
        This is the constructor that initializes all filters and display methods in instance vairables (dict) and  connects to the database.
        The value of each key in dictionary is the corresponded query string. 
        '''
        self.filterDict = {
            "title": "",
            "genre": "",
            "actor": "",
            "country": "",
            "rating": "",
            "director": "",
            "company": "",
            "writer": "",
            
            "scoreRange": "",
            "yearRange": ""
        }
        
        self.displayDict = {
            "sort": "",
            "numOfDisplayRow": ""
        }

        self.connection = self.connect()


    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
                user - username, which is also the name of the database
                password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection


    def getMoviesByFilters(self):
        '''
        Execute the query string on database.

        RETURN:
        a list of Movie objects which satisfy all the filters
        '''
        try:
            cursor =  self.connection.cursor()
            query = self.createQuery()
            cursor.execute(query)
            resultMovie = cursor.fetchall()
            moviesList = []
            for i in range(len(resultMovie)):
                movieObject = Movie(resultMovie[i])
                moviesList.append(movieObject)
            self.connection.close()
            return moviesList
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None


    def createQuery(self):
        '''
        This function forms the complex query by combining all the query strings in the filterDic and displayDic. 

        RETURN:
        a complete query string that can be executed
        '''
        queryHead = "SELECT * FROM movies WHERE "
        query = queryHead
        
        for filter in self.filterDict: 
            if not self.filterDict[filter]  == "":
                query = query + self.filterDict[filter] + "AND "
        
        #Slice off the last extra " AND "
        if len(query) > len(queryHead):
            query = query[:-5]      
        
        for tail in self.displayDict:
            if not self.displayDict[tail] == "":
                query = query + " " + self.displayDict[tail]
        
        return query
            
            
    def setFilterTitle(self, title):
        '''
        Settor function for the "title" filter in filterDic.

        PARAMETERS:
        title - the title of the movie (str)
        '''
        self.filterDict["title"] = "Title LIKE '%" + title + "%' "


    def setFilterGenre(self, genre):
        '''
        Settor function for the "genre" filter in filterDic.

        PARAMETERS:
        genre - the genre of the movie (str)
        '''
        self.filterDict["genre"] = "Genre LIKE '%" + genre + "%' "


    def setFilterActor(self, actorName):
        '''
        Settor function for the "actor" filter in filterDic.

        PARAMETERS:
        actorName - the name of the actor (str)
        '''
        self.filterDict["actor"] = "Star LIKE '%" + actorName + "%' "


    def setFilterCountry(self, country):
        '''
        Settor function for the "country" filter in filterDic.

        PARAMETERS:
        country - the name of the country (str)
        '''
        self.filterDict["country"] = "Country LIKE '%" + country + "%' "


    def setFilterRating(self, rating):
        '''
        Settor function for the "rating" filter in filterDic.

        PARAMETERS:
        rating - the score of the moive (str)
        '''
        if rating in ["G", "NC-17", "PG", "PG-13", "R", "TV-14", "TV-MA", "TV-PG"]:
            self.filterDict["rating"] = "Rating = '" + rating +"' "
        else:
            print("The rating you entered is invalide, avaliable rating filters includ: G, NC-17, PG, PG-13, R, TV-14, TV-MA, TV-PG.")


    def setFilterDirector(self, directorName):
        '''
        Settor function for the "director" filter in filterDic.

        PARAMETERS:
        directorName - the name of the director(str)
        '''
        self.filterDict["director"] = "Director LIKE '%" + directorName + "%' "
        

    def setFilterWriter(self, writerName):
        '''
        Settor function for the "writer" filter in filterDic.

        PARAMETERS:
        writerName - the name of the writer (str)
        '''
        self.filterDict["writer"] = "Writer LIKE '%" + writerName + "%' "


    def setFilterCompany(self, company):
        '''
        Settor function for the "company" filter in filterDic.

        PARAMETERS:
        company - the name of the company (str)
        '''
        self.filterDict["company"] = "Company LIKE '%" + company + "%' "


    def setYearRange(self, start, end):
        '''
        Settor function for the "yearRange" filter in filterDic.

        PARAMETERS:
        start -  low end of the year intervals (str)
        end -  high end of the year intervals (str)
        '''
        if 1979 < int(start) <= int(end) < 2022:
            self.filterDict["yearRange"] = "ReleasedYear BETWEEN " + start + " AND " + end + " "
        else:
            print("Our data covers movies from 1980 to 2021, please enter a valid interval.")


    def setScoreRange(self, start, end):
        '''
        Settor function for the "scoreRange" filter in filterDic.

        PARAMETERS:
        start- the float low end of the score intervals (str)
        end - the float high end of the score intervals (str)
        '''		
        if 1 < int(start) <= int(end) < 10:
            self.filterDict["scoreRange"] = "ImdbScore BETWEEN " + start + " AND " + end + " "
        else:
            print("Our data covers movies with IMDB scores from 1 to 10, please enter a valid interval.")


    def setSortByYear(self, order):
        '''
        Setter function to sort movies according to the "ReleasedYear" in descending (DESC) or
        ascending (ASC) order

        PARAMETERS:
        order -  order of the movie, can be "DESC" or "ASC"(str)
        '''
        self.displayDict["sort"] = "ORDER BY ReleasedYear " + order


    def setSortByScore(self, order):
        '''
        Setter function to sort movies according to the "ImdbScore" in descending (DESC) or
        ascending (ASC) order

        PARAMETERS:
        order - order of the movie, can be "DESC" or "ASC"(str)
        '''
        self.displayDict["sort"] = "ORDER BY ImdbScore " + order
    
    
    def setnumOfDisplayRows(self, number):
        '''
        Setter function to limit how many rows of result we want from the Database.

        PARAMETERS:
        number - number of the rows we want to display
        '''
        if int(number) > 0:
            self.displayDict["numOfDisplayRow"] = "LIMIT " + number
        else:
            print("Please enter a positive integer.")

 
def main():
    #Test the constructor implementation
    testDDB = DataSource()
    print("Initilized Dictionary: " + str(testDDB.filterDict) + " and " + str(testDDB.displayDict))
    
    #Test the creation of query
    testDDB.setFilterCountry("Japan")
    testDDB.setYearRange("1990","2000")
    testDDB.setFilterGenre("Action")
    testDDB.setScoreRange("6","9")
    testDDB.setSortByYear("ASC")
    testDDB.setnumOfDisplayRows("3")
    query = testDDB.createQuery()
    print("Formed the query: " + query)
    
    #Test the connection with the database and execution of query
    print(testDDB.getMoviesByFilters())
        
    testDDB.connection.close()
        
        
if __name__ == '__main__':
	main()
 