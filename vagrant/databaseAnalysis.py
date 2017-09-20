#!/usr/bin/env python3

import psycopg2


# Question 1 and 2 require view: article_views
"""
CREATE VIEW article_views AS
SELECT COUNT(path),
       articles.slug,
       articles.title,
       articles.author
    FROM articles
    INNER JOIN log
    ON articles.slug
    LIKE REPLACE(path, '/article/', '')
    GROUP BY articles.slug, articles.id
    ORDER BY count DESC;
"""


# Question 1: the top 3 articles
QUESTION1 = """
SELECT * FROM article_views ORDER BY count DESC LIMIT %(limit)s;
"""


# Question 2: authors ranked by article views
QUESTION2 = """
SELECT SUM(named_authors.count), named_authors.name FROM
(
    SELECT article_views.count, authors.name FROM article_views
    INNER JOIN authors
    ON article_views.author = authors.id
)
AS named_authors
GROUP BY named_authors.name
ORDER BY sum DESC;
"""


# Question 3 requires view: dailyStatus
"""
CREATE VIEW daily_status AS
SELECT COUNT(status),
          status,
          LEFT(CAST(time AS TEXT), 10)
   AS day
   FROM log
   GROUP BY day, status;
"""


# Question 3: days with error rates greater than 1%
QUESTION3 = """
SELECT * FROM
    (SELECT totals.day, ((errors.count / totals.sum) * 100) AS errorRate  --4
    FROM
        (SELECT SUM(count), day FROM dailyStatus GROUP BY day)            --1
        AS totals
        INNER JOIN                                                        --3
        (SELECT count, day FROM dailyStatus WHERE status='404 NOT FOUND') --2
        AS errors
        ON totals.day = errors.day
    ) AS percents
WHERE percents.errorRate > 1 ORDER BY day DESC;                           --5
"""
# 1 Calculate the total number of requests made each day by
#   summing together requests with either response (type 404 and 200)
# 2 Select out the number of requests that were errors made
#   each day (type 404 only)
# 3 Join the total requests and error requests from each day
#   into a single row
# 4 Calculate the error rate by dividing each days error
#   count by the total request count, then multiplying by
#   100 to get a percent
# 5 Only keep rows that have an error rate greater than 1%,
#   and order them


def TopArticles(count):
    conn, cursor = connect_to_db('news')
    cursor.execute(QUESTION1, {"limit": count})

    print("\nTOP " + str(count) + " ARTICLES")
    for row in cursor:
        print('"' + row[2] + '" -- ' + str(row[0]) + ' views')

    conn.close()


def TopAuthors():
    conn, cursor = connect_to_db('news')
    cursor.execute(QUESTION2)

    print("\nTOP AUTHORS")
    for row in cursor:
        print('"' + str(row[1]) + '" -- ' + str(row[0]) + ' views')

    conn.close()


def HighErrorRates():
    conn, cursor = connect_to_db('news')
    cursor.execute(QUESTION3)

    print("\nHIGH ERROR RATES")
    for row in cursor:
        print(str(row[0]) + ' -- ' + str(format(row[1], "0.2f")) + '% errors')

    conn.close()


def connect_to_db(db_name):
    try:
        conn = psycopg2.connect('dbname=' + str(db_name))
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("Error connecting to database...")


if __name__ == '__main__':
    # Run the queries
    print("Starting logs analysis...")
    TopArticles(3)
    TopAuthors()
    HighErrorRates()
