import pandas as pd 
import pymssql 

from decouple import config as cfg  
from sqlalchemy import text, create_engine 
from config import sql_cfg

SQL_USER = sql_cfg["SQL_USER"]
SQL_PASSWORD = sql_cfg["SQL_PWD"]
SQL_SERVER = sql_cfg["SQL_SERVER"]
SQL_DB = sql_cfg["SQL_DATABASE"]

sql_db_url = f"mssql+pymssql://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DB}"
sql_query_template = "SELECT * FROM {};"

sql_view = "Reporting.vw_OPS_Scorecard_MES_COMPLIANCE_Summ"

engine = create_engine(sql_db_url)
with engine.connect() as conn:
    df = pd.read_sql(sql_query_template.format(sql_view), engine) 
print(df) 