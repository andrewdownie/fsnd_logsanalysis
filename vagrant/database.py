import psycopg2

# Question 1 and 2 require view: article_views
"""
CREATE VIEW article_views AS 
SELECT COUNT(REPLACE(path, '/article/', '')), articles.slug, articles.title, articles.author 
    FROM articles 
    INNER JOIN log 
    ON articles.slug 
    LIKE REPLACE(path, '/article/', '') 
    GROUP BY articles.slug, articles.id 
    ORDER BY count DESC;
"""

#Question 1: the top 3 articles
QUESTION1 = """
SELECT * FROM article_views ORDER BY count DESC {limit};
"""

#Question 2: authors ranked by article views
QUESTION2 = """
SELECT SUM(count), author FROM article_views GROUP BY author ORDER BY sum DESC;
"""


# Question 3 requires view: dailyStatus
"""
CREATE VIEW dailyStatus AS SELECT COUNT(status), status, LEFT(CAST(time AS TEXT), 10) AS day FROM log GROUP BY day, status;
"""

#Question 3: days with error rates greater than 1%
QUESTION3 = """
SELECT * FROM 
    (SELECT totals.day, (errors.count / totals.sum) AS percent FROM         -- 4) Calculate the error rate by dividing each days error count by the total request count
        (SELECT SUM(count), day FROM dailyStatus GROUP BY day)              -- 1) Calculate the total number of requests made each day by summing together both response types (404 and 200) 
            AS totals 
        INNER JOIN                                                          -- 3) Join the total number of requests made and number of requests that were errors using the day to match them up 
        (SELECT count, day FROM dailyStatus WHERE status='404 NOT FOUND')   -- 2) Select out the number of requests that were errors made each day (type 404 only)
            AS errors 
        ON totals.day = errors.day
    ) AS percents 
WHERE percents.percent > 0.01 ORDER BY day DESC;                            -- 5) Only keep rows that have an error rate greater than 1%, and order them

"""

def TopArticles(conn, count):
    print("\nTOP " + str(count) + " ARTICLES")
    q1 = QUESTION1.replace("{limit}", "LIMIT " + str(count))
    cursor = conn.cursor()
    cursor.execute(q1)
    #results = cursor.fetchall()
    #print(results)
    for row in cursor:
        print( '"' + row[2] + '" -- ' + str(row[0]) + ' views')


def TopAuthors(conn):
    print("\nTOP AUTHORS")
    cursor = conn.cursor()
    cursor.execute(QUESTION2)
    results = cursor.fetchall()
    print(results)


def HighErrorRates(conn):
    print("\nHIGH ERROR RATES")
    cursor = conn.cursor()
    cursor.execute(QUESTION3)
    results = cursor.fetchall()
    print(results)


def get_con():
    return psycopg2.connect('dbname=news')



conn = get_con()

print("Connected...")
TopArticles(conn, 3)
#TopAuthors(conn)
#HighErrorRates(conn)


"""
cursor.execute(QUESTION2)
print(cursor.fetchall())
"""

