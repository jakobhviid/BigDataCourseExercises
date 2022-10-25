import pymysql

# IP address of the MySQL database server, that is already started with datahub
Host = "mysql"  
# User name of the database server (root is required to enable manipulation of the database)
User = "root"       
# Password for the database user
Password = "datahub"
# database you want to use
database = "datahub"
conn  = pymysql.connect(host=Host, user=User, password=Password, database=database)
cur  = conn.cursor() 

# Your task is to replace the following code to ingest the individual words of Alice in Wonderland
# First you need to read the file (the file is loaded into the root of the container at ./alice-in-wonderland.txt)

# Then you must split the content of the file into individual words

# Then create a table called alice and insert the individual words as (id, word) into the table



## Example of interacting with the database
query = f"CREATE TABLE IF NOT EXISTS test (a int)"
cur.execute(query)

PRODUCT_ID = 1201
price = 10000
PRODUCT_TYPE = 'PRI'

query = f"INSERT INTO test (a) VALUES ('{PRODUCT_ID}')"
cur.execute(query)
print(f"{cur.rowcount} details inserted")
conn.commit()
conn.close()