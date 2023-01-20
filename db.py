import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user='postgres',
    password='mysecretpassword')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS emp;')
cur.execute('CREATE TABLE emp (id serial PRIMARY KEY,'
            'name varchar (150) NOT NULL,'
            'email varchar (50) NOT NULL,'
            'salary integer NOT NULL,'
            'feedback text,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table

cur.execute('INSERT INTO emp (name, email, salary, feedback)'
            'VALUES (%s, %s, %s, %s)',
            ('John Smith',
             'js07@gmail.com',
             1000,
             'Very Good')
            )

cur.execute('INSERT INTO emp (name, email, salary, feedback)'
            'VALUES (%s, %s, %s, %s)',
            ('Anna Karenina',
             'ak001@gmail.com',

             800,
             'Good')
            )

conn.commit()

cur.close()
conn.close()
