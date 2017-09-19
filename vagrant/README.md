# To run this program
Within the vagrant environment run the command:
    `python3 databaseAnalysis.py`


# Program design:
The sql commands are at the top of the file, including the creation of views.
The database is connected to, and the commands are executed at the bottom of the project where each question has a function dedicated to answer it.


# The views needed for this program are:
## article_views for questions 1 and 2
`CREATE VIEW article_views AS
SELECT COUNT(REPLACE(path, '/article/', '')),
       articles.slug,
       articles.title,
       articles.author
    FROM articles
    INNER JOIN log
    ON articles.slug
    LIKE REPLACE(path, '/article/', '')
    GROUP BY articles.slug, articles.id
    ORDER BY count DESC;`

## dailyStatus for question 3
`CREATE VIEW dailyStatus AS
SELECT COUNT(status),
          status,
          LEFT(CAST(time AS TEXT), 10)
   AS day
   FROM log
   GROUP BY day, status;`



