# About this project
This project requires vagrant, to setup vagrant see: <link to udacity vagrant setup instructions>

TODO 
TODO 
TODO 
TODO 
Describe what the purpose of the project is and what your program does. For example, you could mention that your Python script uses psycopg2 to query a mock PostgreSQL database for a fictional news website. You could discuss how the news database is structured, and what questions your script answers in the report it generates.

# Project Setup
## Setting up the vagrant environment
### Download the vagrant environment file:
Download the vagrant environment file, and put it into a folder (make sure to save it without a file extension).
https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile
### Download and start the vagrant environment:
With a terminal, navigate to the folder you created, with the vagrant environment file, and run the following command:
```bash
vagrant up
```
### Ssh into the vagrant environment:
Once the ```vagrant up``` command has completed, run:
```bash
vagrant ssh
```

## Setting up the database
### Download the newsdata.zip file:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

### Extract the newsdata.sql file: 
Extract the newsdata.sql file into the vagrant folder from the newsdata.zip.

From within a ssh session with the vagrant environment, run the command line command:
```
psql -d news -f newsdata.sql
```

## Creating the required views
Two views will need to be created in the _news_ database before this program can be run. These views are: article_views and daily_status, and they are listed at the bottom of this readme. 

One method to create the required article_views and daily_status views is from within environment vagrant, enter the database interactively from the command line with: 
```sql
psql -d news
```

and then copy and paste, one at a time, the sql at the bottom of this file to create the article_views and daily_status views.


# Running this project 
```python
python3 databaseAnalysis.py
```


# Program design:
The sql commands are at the top of the file, including the creation of views.


# The views needed for this program are:

## article_views for questions 1 and 2
```sql
CREATE VIEW article_views AS
SELECT COUNT(path),
       articles.slug,
       articles.title,
       articles.author
    FROM articles
    INNER JOIN log
    ON '/article/' || articles.slug = path
    LIKE REPLACE(path, '/article/', '')
    GROUP BY articles.slug, articles.id
    ORDER BY count DESC;
```

## dailyStatus for question 3
```sql
CREATE VIEW daily_status AS
SELECT COUNT(status),
          status,
          LEFT(CAST(time AS TEXT), 10)
   AS day
   FROM log
   GROUP BY day, status;
```



