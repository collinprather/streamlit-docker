import psycopg2
from sklearn.datasets import load_boston
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import os

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(load_dotenv())
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

# loading and saving boston.csv
boston = load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)
y = pd.DataFrame(boston.target, columns=["PRICE"])
df = pd.concat([X, y], axis=1)
df.to_csv("boston.csv", index=False)

conn = psycopg2.connect(host='postgres',
                       port='5432',
                       dbname=dbname,
                       user=user,
                       password=password
                        )

cur = conn.cursor()

# creating table
cur.execute("drop table if exists boston;")
cur.execute("""
create table boston(
CRIM float,
ZN float,
INDUS float,
CHAS float,
NOX float,
RM float,
AGE float,
DIS float,
RAD float,
TAX float,
PTRATIO float,
B float,
LSTAT float,
PRICE float
);""")
conn.commit()
print("created boston table")

# loading data into table
with open('boston.csv', 'r') as f:
    next(f)    # skip headers
    cur.copy_from(f, 'boston', sep=',')
conn.commit()
print("loaded data into boston table")