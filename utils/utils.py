import functools 
import time

import pymssql 
import pandas as pd 
from sqlalchemy import create_engine, text 
from app import app, cache, TIMEOUT
 
def code_timer(func):
    """
    Print the runtime of the decorated function
    Args:
        func (_type_): _description_
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter() 
        value = func(*args, **kwargs) 
        end_time = time.perf_counter()
        args_0 = None if len(args) == 0 else str(args[0])
        run_time = end_time - start_time 
        print(f"*** Finish {func.__name__!r} with {args_0} in {run_time:.4f} secs")
        return value 
    return wrapper_timer

@code_timer
def sql_conn(cfg):
    SQL_USER = cfg["SQL_USER"]
    SQL_PASSWORD = cfg["SQL_PWD"]
    SQL_SERVER = cfg["SQL_SERVER"]
    SQL_DB = cfg["SQL_DATABASE"]

    sql_db_url = f"mssql+pymssql://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DB}"
    try:
        engine = create_engine(sql_db_url)
        print(f"Engine connection established to SERVER:{SQL_SERVER}-DB:{SQL_DB}!!!")
        return engine  
    except Exception as e:
        print(f"Engine connection failed!!!!")
        print(e)
        return None 

@code_timer
# @cache.memoize(timeout=TIMEOUT)
def get_table(sql_query, engine):
    with engine.connect() as conn:
        df = pd.read_sql(text(sql_query), conn)
    return df 