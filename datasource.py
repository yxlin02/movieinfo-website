import psycopg2
import psqlConfig as config


class Movie:
    '''
    Movie is an object class and Movie objects are included in the list we send to the front end.
    '''

    def __init__(self, movieInfo):
        '''
        This function takes in a entry from the database and creates Movie objects which contain information about the movie.
        '''
        self.title = movieInfo[0]
        self.rating = movieInfo[1]
        self.genre = movieInfo[2]
        self.year = movieInfo[3]
        self.score = movieInfo[4]
        self.director = movieInfo[5]
        self.writer = movieInfo[6]
        self.star = movieInfo[7]
        self.country = movieInfo[8]
        self.company = movieInfo[9]
        self.runtime = movieInfo[10]


class DataSource:
    '''
    DataSource executes all of the queries on the database. It executes by editing the PSQL query string through setter methods.
    It also formats the data to send back to the frontend, in a list of Movie objects.
    '''

    def __init__(self):
        '''
        This is the constructor that initializes empty arrays that are going to contain small pieces of queries and their corresponding values.
		It also connects to the database and has it as an instance variable.

        Note: filterQueryArray contains small pieces of queries with %s place holder, filterValueArray holds the actual user input.
        '''
        self.filterQueryArray = [] 
        self.filterValueArray = [] 
        self.displayQueryArray = []
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
            connection = psycopg2.connect(
                database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection


    def getMoviesByFilters(self):
        '''
        Execute the query string created in createQuery() on database.

        RETURN:
        a list of Movie objects which satisfy all the filters
        '''
        valueTuple = self.convertToTuple()
        try:
            cursor = self.connection.cursor()
            query = self.createQuery()
            cursor.execute(query, valueTuple)
            resultMovie = cursor.fetchall()
            resultMovieList = []
            for i in range(len(resultMovie)):
                movieObject = Movie(resultMovie[i])
                resultMovieList.append(movieObject)
            return resultMovieList

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None


    def convertToTuple(self):
        '''
        This is a helper function that turns the filterValueArray into a tuple.

        RETURN:
        a tuple form of filterValueArray
        '''
        return tuple(self.filterValueArray)


    def createQuery(self):
        '''
        This function forms the complex query by combining all the query strings in filterQueryArray and displayQueryArray. 

        RETURN:
        a complete query string that can be executed
        '''
        
        if len(self.filterQueryArray) == 0:
            query = "SELECT * FROM movies "
        else:
            query = "SELECT * FROM movies WHERE "
        
        for position, queryFilterString in enumerate(self.filterQueryArray):
            if position > 0 :
                query += " AND "
            query += queryFilterString
        
        for postion, queryDisplayString in enumerate(self.displayQueryArray):
            query += "\n"
            query += queryDisplayString

        return query
  
            
    def addFilterTitle(self, title):
        '''
        Add a filter to select movies with a specific title.

        PARAMETERS:
        title - the title of the movie (str)
        '''
        self.filterQueryArray.append("Title LIKE " + "%s")
        formatedInput = "%" + title + "%"
        self.filterValueArray.append(formatedInput)
        

    def addFilterGenre(self, genre):
        '''
        Add a filter to select movies with a specific genre.

        PARAMETERS:
        genre - the genre of the movie (str)
        '''
        self.filterQueryArray.append("Genre LIKE "+ "%s")
        formatedInput = "%" + genre + "%"
        self.filterValueArray.append(formatedInput)


    def addFilterActor(self, actorName):
        '''
        Add a filter to select movies with a specific actor who participated.

        PARAMETERS:
        actorName - the name of the actor (str)
        '''
        self.filterQueryArray.append("Star LIKE " + "%s")
        formatedInput = "%" + actorName + "%"
        self.filterValueArray.append(formatedInput)


    def addFilterCountry(self, country):
        '''
        Add a filter to select movies produced in a specific country.

        PARAMETERS:
        country - the name of the country (str)
        '''
        self.filterQueryArray.append("Country LIKE " + "%s")
        formatedInput = "%" + country + "%"
        self.filterValueArray.append(formatedInput)


    def addFilterRating(self, rating):
        '''
        Add a filter to select movies with a specific rating.

        PARAMETERS:
        rating - the score of the moive (str)
        '''
        if rating in ["G", "NC-17", "PG", "PG-13", "R", "TV-14", "TV-MA", "TV-PG"]:
            self.filterQueryArray.append("Rating = " + "%s")
            self.filterValueArray.append(rating)
        else:
            print("The rating you entered is" + rating)
            print("The rating you entered is invalid, available rating filters include: G, NC-17, PG, PG-13, R, TV-14, TV-MA, TV-PG.")


    def addFilterDirector(self, directorName):
        '''
        Add a filter to select movies with a specific director.

        PARAMETERS:
        directorName - the name of the director(str)
        '''
        self.filterQueryArray.append("Director LIKE " + "%s")
        formatedInput = "%" + directorName + "%"
        self.filterValueArray.append(formatedInput)
        

    def addFilterWriter(self, writerName):
        '''
        Add a filter to select movies with a specific writer.

        PARAMETERS:
        writerName - the name of the writer (str)
        '''
        self.filterQueryArray.append("Writer LIKE " + "%s")
        formatedInput = "%" + writerName + "%"
        self.filterValueArray.append(formatedInput)


    def addFilterCompany(self, company):
        '''
        Add a filter to select movies with a specific company.

        PARAMETERS:
        company - the name of the company (str)
        '''
        self.filterQueryArray.append("Company LIKE " + "%s")
        formatedInput = "%" + company + "%"
        self.filterValueArray.append(formatedInput)


    def addFilterYearRange(self, start, end):
        '''
        Add a filter to select movies released within a specific year range.

        PARAMETERS:
        start -  low end of the year intervals (str)
        end -  high end of the year intervals (str)
        '''
        if 1980 <= int(start) <= int(end) <= 2020:
            self.filterQueryArray.append("ReleasedYear BETWEEN " + "%s" + " AND " + "%s" + " ")
            self.filterValueArray.append(start)
            self.filterValueArray.append(end)
        else:
            print("Our data covers movies from 1980 to 2020, please enter a valid interval.")


    def addFilterScoreRange(self, start, end):
        '''
        Add a filter to select movies with scores within a specific range.

        PARAMETERS:
        start- the low end of the score intervals (int)
        end - the high end of the score intervals (int)
        '''		
        if 1 <= start <= end <= 10:
            self.filterQueryArray.append("ImdbScore BETWEEN " + "%s" + " AND " + "%s" + " ")
            self.filterValueArray.append(start)
            self.filterValueArray.append(end)
        else:
            print("Our data covers movies with IMDB scores from 1 to 10, please enter a valid interval.")


    def addSortByYear(self, order):
        '''
        Add a query to sort the selected movies by released year in ascending or descending order.

        PARAMETERS:
        order -  order of the movie, can be "DESC" or "ASC"(str)
        '''
        if order in ['DESC', 'ASC']:
            self.displayQueryArray.append("ORDER BY ReleasedYear " + order)
        else:
            print("Please enter 'DESC' or 'ASC' for order.")


    def addSortByScore(self, order):
        '''
        Add a query to sort the selected movies by the score in ascending or descending order.

        PARAMETERS:
        order - order of the movie, can be "DESC" or "ASC"(str)
        '''
        if order in ['DESC', 'ASC']:
            self.displayQueryArray.append("ORDER BY ImdbScore " + order)
        else:
            print("Please enter 'DESC' or 'ASC' for order.")

    
    def addNumOfDisplayRows(self, number):
        '''
        Add a query to limit how many rows of results we want from the Database.

        PARAMETERS:
        number - number of the rows we want to display (int)
        '''
        if number > 0:
            self.displayQueryArray.append("LIMIT " + str(number))
        else:
            print("Please enter a positive integer.")

 
def main():
    '''
    This is a class for testing.
    '''

    # Test the constructor implementation
    testDB = DataSource()
    
    # Test the creation of query
    testDB.addFilterCountry("Japan")
    testDB.addFilterYearRange("1990","2000")
    testDB.addFilterGenre("Action")
    testDB.addFilterScoreRange("6","9")
    testDB.addSortByYear("ASC")
    testDB.addNumOfDisplayRows("3")
    query = testDB.createQuery()
    print("Formed the query: " + query)
    
    # Test the connection with the database and execution of query
    print(testDB.getMoviesByFilters()[0].star)
        
    testDB.connection.close()
        
        
if __name__ == '__main__':
	main()