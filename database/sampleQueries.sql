/* Query 1
- List all the movies that Tom Holland acted in. Using ascending order of released year.
- Meet the user goal that the fan of Tom Holland wants to find all the movies Tom has acted in.
 */

SELECT * FROM movies WHERE Star LIKE '%Tom%Holland%' ORDER BY ReleasedYear ASC;

/*  Query 2
- List top 10 movies with 7 or higher ImdbScore that are relased between 2018 and 2020.
- Restricted to movies that don't need the audiance to be 18 yaers old or above.
- Meet the user goal of finding a recent movie that is highly scored for film club public screening.
 */

SELECT * FROM movies WHERE ImdbScore > 7 AND ReleasedYear BETWEEN 2018 AND 2020 
INTERSECT
SELECT * FROM movies WHERE Rating IN ('G','PG','PG-13') ORDER BY ImdbScore DESC LIMIT 10;


/* Query 3
- List Japanese action movies between 1990 and 2000 with a score between 6 and 9.
- Meet the user goal that a film history student has to find Japanese action movies 20 years ago with for his film class assignment.
 */
SELECT * FROM movies WHERE Country = 'Japan' AND ReleasedYear BETWEEN 1990 AND 2000
INTERSECT
SELECT * FROM movies WHERE Genre = 'Action' AND ImdbScore BETWEEN 6 AND 9 ORDER BY ReleasedYear ASC;


/* Query 4
- List top 30 movies (of scores) that are producted by Warner Brothers with a high Imdb Score.
- Meet the user goal that a film industry worker wants to learn more about high-scored movies produced by a large film compamy.
 */
SELECT * FROM movies WHERE Company LIKE '%Warner%' AND ImdbScore > 7 ORDER BY ImdbScore DESC LIMIT 30;