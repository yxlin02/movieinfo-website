# README

Our dataset only contains less than 8000 entries and the fundamental structure between each type of data is the **name of the movie** followed by **other details about that movie**. Even there are movies that share the same names (we have 7668 entries of the name but 7512 unique values), those movies can be easily distinguished with **other details about that movie** such as **ReleasedYear**, **Country,** and **Director**. Thus, I decided to use one single table and the level of normalization is high enough for this small project. I removed the column of **ReleasedDate** because it provides overly detailed information that users don't need and partially overlapped with **ReleasedYear**. The users of movie review websites usually prefer only the **ReleasedYear** over the **ReleasedDate**. Additionally, I removed the column of **UserVotes** because the data is only rendered to the hundreds, and there are many entries that do not have this item. Also, I deleted the columns **Budget** and **Revenue** because they are not the interests of our specified user roles and there is ambiguity in the currency of that data. Lastly, I choose the datatype `varchar` to store all the data with characters (for example, title, director) because all of the entries are short with various lengths and I want to make all of them consistent (same datatype). I used `smallint` for **ReleasedYear** because PostgreSQL doesn't support the datatype `year`. I used `real` for **ImbdScore** and **Runtime** because they have decimals.

**Query 1**

- This query will list all the movies that Tom Holland acted in and sorted them in ascending order by released year.
- This query fulfills the user goal that the fans can find all the movies Tom has acted in and watch them again and again.

**Query 2**

- This query will list the top 10 movies (according to IMBD score) with 7 or higher IMBD Scores that are released between 2018 and 2020. Furthermore, it also only shows movies with G, PG, and PG-13 ratings.
- This query fulfills the user goal that a movie club member wants to find a recent movie with a high score for public screening.

**Query 3**

- This query will list all the Japanese movies with the Action genre that are released between 1990 and 2000. All the movies selected have an IMBD Score between 6 and 9, and they are sorted in ascending order by released year.
- This query fulfills the user goal that a film history student needs to find a Japanese action movie 20 years ago for his film class assignment.

**Query 4**

- This query will list the top 30 (of scores) movies produced by Warner Brothers.
- This query fulfills the user goal that a film industry worker wants to learn more about high-scored movies produced by a large film company.