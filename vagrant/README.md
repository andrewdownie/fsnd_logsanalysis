# About this project
This project requires vagrant, and virtual box:
https://www.vagrantup.com/ 
https://www.virtualbox.org/wiki/Downloads


## Outline
The purpose of this project it to perform analysis on a mock news website database using sql. To do this, the python script databaseAnalysis.py uses psycopg2 makes sql queries to a psql database.

### The database being queried has three tables:
1. articles - Holds article metadata, as well as the article themselves.
2. authors - Holds information about authors that write articles.
3. log - Holds information about accesses to the website.

### The three analysis on the database:
The three analysis on the database that this program performs are:
1. Top 3 articles by number of views.
2. Authors ranked by the sum of all of their articles views.
3. Days that experienced greater than 1% error rates, in terms of http responses.


# Getting started with this project
## Setting up the vagrant environment
It is assumed you already have virtual box and vagrant installed.
### Download the vagrant environment file:
Download the vagrant environment file, and put it into a folder (make sure to save it without a file extension).
https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile
### Download and start the vagrant environment:
With a terminal, navigate to the folder you created with the vagrant environment file, and run the following command:
```bash
vagrant up
```
### Ssh into the vagrant environment:
Once the ```vagrant up``` command has completed, run:
```bash
vagrant ssh
```
You are now ready to setup the database.
## Setting up the database
### Download the newsdata.zip file:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

### Extract the newsdata.sql file: 
Extract the newsdata.sql file from the newsdata.zip into the vagrant folder you created earlier.

From within a terminal ssh session with the vagrant environment, navigate to ```/vagrant``` and run the command line command:
```
psql -d news -f newsdata.sql
```

## Creating the required views
Two views will need to be created in the _news_ database before this program can be run. These views are: article_views and daily_status, and they are listed at the bottom of this readme. 

One method to create the required article_views and daily_status views is from within environment vagrant, enter the database interactively from the command line with: ```psql -d news``` and then copy and paste, the sql code to create the two views. The sql code can be found at the bottom of this file.


# Running this project 
make sure the ```databaseAnalysis.py script from this repo is in the vagrant folder, and run:
```python
python3 databaseAnalysis.py
```


# The views needed for this program are:

## article_views for questions 1 and 2
```sql
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



