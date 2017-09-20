# Before running this program
Two views will need to be created in the database before this program can be run. These views are: article_views and daily_status, and they are listed at the bottom of this readme. 

One method to create the required article_views and daily_status views is from within environment vagrant, enter the database interactively from the command line with: 
`psql -d news`

and then copy and paste, one at a time, the sql at the bottom of this file to create the article_views and daily_status views.


# To run this program, within the vagrant environment run the command:
`python3 databaseAnalysis.py`


# Program design:
The sql commands are at the top of the file, including the creation of views.


# The views needed for this program are:

## article_views for questions 1 and 2
CREATE VIEW article_views AS
SELECT COUNT(REPLACE(path, '/article/', '')),
       articles.slug,
       articles.title,
       articles.author
    FROM articles
    INNER JOIN log
    ON articles.slug
    LIKE REPLACE(path, '/article/', '')
    GROUP BY articles.slug, articles.id
    ORDER BY count DESC;

## dailyStatus for question 3
CREATE VIEW daily_status AS
SELECT COUNT(status),
          status,
          LEFT(CAST(time AS TEXT), 10)
   AS day
   FROM log
   GROUP BY day, status;



