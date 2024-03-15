# BeforeMain.py must be run to create the database and tables before running the Main.py
# You must enter your user password for the PostgreSQL database in the userPassword variable.

import psycopg2

userPassword = ("secret")  # enter your password
conn = None
try:
    conn = psycopg2.connect(host = "localhost",
                            database="postgres",
                            user="postgres",
                            password=userPassword)
    conn.autocommit = True
    cur = conn.cursor()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

cur.execute("CREATE DATABASE wpsm;")

conn.commit()

cur.close()
conn = conn.close()

try:
    conn = psycopg2.connect(host = "localhost",
                            database="wpsm",
                            user="postgres",
                            password=userPassword)
    cursor = conn.cursor()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

cursor.execute("""CREATE TABLE settings_info(
                id SERIAL PRIMARY KEY NOT NULL,
                theme CHARACTER VARYING NOT NULL,
                language CHARACTER VARYING NOT NULL)
            """)

cursor.execute("""CREATE TABLE saved_message(
                title CHARACTER VARYING PRIMARY KEY NOT NULL,
                message CHARACTER VARYING [] NOT NULL,
                auto_timer BOOLEAN NOT NULL,
                wait_time INTEGER,
                repetition INTEGER NOT NULL,
               contacts CHARACTER VARYING [] NOT NULL)
            """)

cursor.execute("""CREATE TABLE contacts(
                tell_number CHARACTER VARYING PRIMARY KEY NOT NULL,
                full_name CHARACTER VARYING NOT NULL)
            """)

conn.commit()

cursor.close()
conn = conn.close()
