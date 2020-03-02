import psycopg2
from sklearn.datasets import load_boston
import pandas as pd

# loading and saving boston.csv
boston = load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)
y = pd.DataFrame(boston.target, columns=["PRICE"])
df = pd.concat([X, y], axis=1)
df.to_csv("boston.csv", index=False)

# creating table and loading csv into postgres
conn = psycopg2.connect(host='postgres',   # made availble by network created automatically by do$
                       port='5432',        # defined in docker-compose.yml
                       dbname='streamlit_db',    # defined in postgres.env
                       user='docker',      # defined in postgres.env
                       password='docker'   # not sure where defined
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