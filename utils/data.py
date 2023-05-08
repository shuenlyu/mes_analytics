from .config import sql_cfg, tables_cfg 
from .utils import code_timer, sql_conn, get_table 

from collections import OrderedDict
import pandas as pd 

from app import app, cache, TIMEOUT
import inspect 


@code_timer
@cache.memoize()
def all_tables():
    sql_views = OrderedDict() 
    sql_query_template = "SELECT * FROM {};"
    engine = sql_conn(sql_cfg) 

    for key, view in tables_cfg.items():
        sql_views[f"TABLE_{key.upper()}"] = get_table(sql_query_template.format(view), engine)
    
    """debugging block to print the frame where this function is being called"""
    # caller_frame = inspect.getsource(inspect.currentframe().f_back)
    # print(caller_frame)
    return sql_views    
 
#fetch all data from sql server 
sql_views = all_tables()

rcv_df               = sql_views.get("TABLE_RCV")
shp_df               = sql_views.get("TABLE_SHP")
rcv_shp_df           = sql_views.get("TABLE_RCV_SHP")
wip_df               = sql_views.get("TABLE_WIP")
tat_df               = sql_views.get("TABLE_TAT")
dmr_df               = sql_views.get("TABLE_DMR")
eTraveler_df         = sql_views.get("TABLE_ETRAVELER")
mes_proc_df          = sql_views.get("TABLE_MES_PROC")
mes_wait_df          = sql_views.get("TABLE_MES_WAIT")
mes_rcv_df           = sql_views.get("TABLE_MES_RCV")
mes_shp_df           = sql_views.get("TABLE_MES_SHP")
mes_compliance_df    = sql_views.get("TABLE_MES_COMPLIANCE")


##data transformation 
mes_compliance_df["WorkWeek_RW"] = pd.to_datetime(mes_compliance_df.Kit_Box_Date).apply(lambda x: x.weekofyear)

'''
tables and their columns
rcv_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'Total_WOs' 'Total_Barcodes' 'Total_Bags' 'Total_Qty'
 'Total_Value_USD']
shp_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'Late_OnTime' 'Total_WOs' 'Total_Barcodes'
 'Total_Bags' 'Total_Qty' 'Total_Value_USD']
rcv_shp_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'Late_OnTime' 'Event_Type' 'Event_Name' 'Total_WOs'
 'Total_Barcodes' 'Total_Bags' 'Total_Qty' 'Total_Value_USD']
wip_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'Late_OnTime' 'Total_WOs' 'Total_Barcodes'
 'Total_Bags' 'Total_Qty' 'Total_Value_USD']
tat_df.columns: ['Location_Code' 'Location_Name' 'WorkYear' 'WorkMonth' 'WorkWeek' 'Date'
 'DOW_Name' 'DayNum' 'WOS' 'Late_OnTime' 'Avg_TAT_Days' 'Days_Early_Late'
 'Dollar_Value']
dmr_df.columns: ['LocationCode' 'Location_Name' 'Work_year' 'Work_Month' 'WorkWeek'
 'DayOfWeek' 'DayNum' 'DateOpened' 'DMRType' 'ProblemCategory' 'DMR_Count']
eTraveler.columns:['locationID' 'locationName' 'DATE' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'Workweek' 'status' 'Barcode_Count']
mes_proc_df.columns: ['LocationCode' 'location_Name' 'RowType' 'Date' 'Work_year' 'Work_Month'
 'WorkWeek' 'DayOfWeek' 'DayNum' 'ProcHours']
mes_wait_df.columns: ['LocationCode' 'location_Name' 'RowType' 'Date' 'Work_year' 'Work_Month'
 'WorkWeek' 'DayOfWeek' 'DayNum' 'ProcHours']
mes_rcv_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'MES_SHP_BC']
mes_shp_df.columns: ['LocationCode' 'Location_Name' 'Date' 'Work_Year' 'Work_Month' 'DOW_Name'
 'DayNum' 'WorkWeek' 'MES_SHP_BC']
mes_compliance_df.columns: ['location_name' 'Work_Order_No' 'Work_Order_Split' 'WO_Num'
 'Kit_Box_Date' 'OverrideDate' 'WorkWeek' 'WorkYear' 'DayNum'
 'Action_Status' 'Override_by']
'''

##global slicer values
@code_timer
@cache.memoize(timeout=TIMEOUT)
def global_slicer_data():
    slicer_work_week = pd.concat([
        rcv_df.WorkWeek, 
        shp_df.WorkWeek, 
        rcv_shp_df.WorkWeek, 
        wip_df.WorkWeek, 
        tat_df.WorkWeek, 
        dmr_df.WorkWeek, 
        eTraveler_df.Workweek,
        mes_proc_df.WorkWeek,
        mes_wait_df.WorkWeek, 
        mes_rcv_df.WorkWeek, 
        mes_shp_df.WorkWeek, 
        mes_compliance_df.WorkWeek_RW
    ], ignore_index=True).astype("int64").drop_duplicates().sort_values().to_list() 
    
    slicer_work_year = pd.concat([
        rcv_df.Work_Year,
        shp_df.Work_Year,
        rcv_shp_df.Work_Year, 
        wip_df.Work_Year,
        tat_df.WorkYear, 
        dmr_df.Work_year, 
        eTraveler_df.Work_Year,
        mes_proc_df.Work_year,
        mes_wait_df.Work_year,
        mes_rcv_df.Work_Year,
        mes_shp_df.Work_Year,
        mes_compliance_df.WorkYear], ignore_index=True).drop_duplicates().sort_values().to_list()
    
    slicer_locations = pd.concat([
        rcv_df.Location_Name, 
        shp_df.Location_Name, 
        rcv_shp_df.Location_Name, 
        wip_df.Location_Name, 
        tat_df.Location_Name, 
        dmr_df.Location_Name, 
        eTraveler_df.locationName, 
        mes_proc_df.location_Name, 
        mes_wait_df.location_Name, 
        mes_rcv_df.Location_Name, 
        mes_shp_df.Location_Name, 
        mes_compliance_df.location_name
    ], ignore_index=True).drop_duplicates().sort_values().to_list() 
    return slicer_work_year, slicer_work_week, slicer_locations

slicer_work_year, slicer_work_week, slicer_location = global_slicer_data()