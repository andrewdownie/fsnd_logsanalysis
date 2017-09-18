import psycopg2

"""
def get_con():
    return psycopg2.connect(
        "dbname='WelcatWorking'\
        user='welcatreaders'\
        host='welcat-working.cz3evk2oqbiz.us-west-2.rds.amazonaws.com'\
        port='5432' \
        password='ThatBackendTho'")
"""


def get_con():
    return psycopg2.connect('dbname=news')



conn = get_con()
cursor = conn.cursor()

cursor.execute("SELECT * FROM articles;")
print(cursor.fetchall())

