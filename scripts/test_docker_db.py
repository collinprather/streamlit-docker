import psycopg2
from dotenv import find_dotenv, load_dotenv
import os

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(load_dotenv())
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(host='postgres',
                       port='5432',
                       dbname=dbname,
                       user=user,
                       password=password
                        )

cur = conn.cursor()
cur.execute("select * from boston limit 5;")
result = cur.fetchall()
print(result)

print("now converting to pandas")
cur.execute("select * from boston limit 0;")
col_names = [desc[0] for desc in cur.description]
print(col_names)

import pandas as pd
df = pd.DataFrame(result, columns=col_names)
print(df)

cur.close()
conn.close()