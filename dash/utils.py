import os
import pg8000

from sky import Sky
from google.cloud.sql.connector import connector

BB_API_KEY = os.getenv('BB_API_KEY')

# Loading sky api client 
sky = Sky(
    api_key=BB_API_KEY,
    credentials={
    "client_id":os.getenv('CLIENT_ID'),
    "client_secret":os.getenv('CLIENT_SECRET'),
    })

# Function to connect to Cloud SQL db
def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        os.getenv("INSTANCE_CONNECTION_NAME"),
        "pg8000",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME"),
    )
    return conn

def stringToComparison(comparison_string):
    return (comparison_string or '') + "%"

def calldb(stmt, request_type="single"):
    conn = getconn()
    cur = conn.cursor()
    cur.execute(stmt)
    if request_type == "single":
        result = cur.fetchone()
    else:
        result = cur.fetchall()
    return result

def toTitleCase(param):
    if isinstance(param, str):
        return param.title()
    return None

def toLowerCase(param):
    if isinstance(param, str):
        return param.lower()
    return None