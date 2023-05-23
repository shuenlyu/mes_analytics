from .config import sql_cfg, tables_cfg 
from .utils import code_timer, sql_conn, get_table, view_column_name_mapping 

from collections import OrderedDict
import pandas as pd 

from app import app, cache, TIMEOUT
import inspect 

def date_format(origin_df):
    input_df = origin_df.copy()
    if "date" in input_df.columns:
        # input_df.date = pd.to_datetime(input_df.date).dt.strftime("%b %d")
        input_df.date = pd.to_datetime(input_df.date).dt.date
    elif "kit_box_date" in input_df.columns:
        #transform for mes df compliance dataframe
        input_df.kit_box_date = pd.to_datetime(input_df.kit_box_date).dt.date        
    elif "dateopened" in input_df.columns:
        input_df.dateopened = pd.to_datetime(input_df.dateopened).dt.date
    return input_df


@code_timer
@cache.memoize(timeout=TIMEOUT)
def all_tables():
    sql_views = OrderedDict() 
    sql_query_template = "SELECT * FROM {};"
    engine = sql_conn(sql_cfg) 

    for key, view in tables_cfg.items():
        origin_df =  get_table(sql_query_template.format(view), engine)
        #Data transformation
        #rename columns to generize all the name to lower case and make the name for workweek workyear, 
        # locationname the same for all the views 
        name_mapping = view_column_name_mapping(origin_df.columns.values)
        origin_df.rename(columns=name_mapping, inplace=True)
        
        #mes df compliance transform
        if "kit_box_date" in origin_df.columns: 
            origin_df["work_week_rw"] = pd.to_datetime(origin_df.kit_box_date).apply(lambda x: x.weekofyear)
            
        sql_views[f"TABLE_{key.upper()}"] = date_format(origin_df)
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
otd_df               = sql_views.get("TABLE_OTD")
tat_df               = sql_views.get("TABLE_TAT")
dmr_df               = sql_views.get("TABLE_DMR")
eTraveler_df         = sql_views.get("TABLE_ETRAVELER")
mes_proc_df          = sql_views.get("TABLE_MES_PROC")
mes_wait_df          = sql_views.get("TABLE_MES_WAIT")
# mes_proc_wait_df     = sql_views.get("TABEL_MES_PROC_WAIT")
mes_rcv_df           = sql_views.get("TABLE_MES_RCV")
mes_shp_df           = sql_views.get("TABLE_MES_SHP")
mes_compliance_df    = sql_views.get("TABLE_MES_COMPLIANCE")


##data transformation 
# mes_compliance_df["work_week_rw"] = pd.to_datetime(mes_compliance_df.kit_box_date).apply(lambda x: x.weekofyear)

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
        rcv_df.work_week, 
        shp_df.work_week, 
        rcv_shp_df.work_week, 
        wip_df.work_week, 
        tat_df.work_week, 
        dmr_df.work_week, 
        eTraveler_df.work_week,
        mes_proc_df.work_week,
        mes_wait_df.work_week, 
        mes_rcv_df.work_week, 
        mes_shp_df.work_week, 
        mes_compliance_df.work_week_rw
    ], ignore_index=True).astype("int64").drop_duplicates().sort_values().to_list() 
    
    slicer_work_year = pd.concat([
        rcv_df.work_year,
        shp_df.work_year,
        rcv_shp_df.work_year, 
        wip_df.work_year,
        tat_df.work_year, 
        dmr_df.work_year, 
        eTraveler_df.work_year,
        mes_proc_df.work_year,
        mes_wait_df.work_year,
        mes_rcv_df.work_year,
        mes_shp_df.work_year,
        mes_compliance_df.work_year], ignore_index=True).drop_duplicates().sort_values().to_list()
    
    slicer_locations = pd.concat([
        rcv_df.location_name, 
        shp_df.location_name, 
        rcv_shp_df.location_name, 
        wip_df.location_name, 
        tat_df.location_name, 
        dmr_df.location_name, 
        eTraveler_df.location_name, 
        mes_proc_df.location_name, 
        mes_wait_df.location_name, 
        mes_rcv_df.location_name, 
        mes_shp_df.location_name, 
        mes_compliance_df.location_name
    ], ignore_index=True).drop_duplicates().sort_values().to_list()
     
    return slicer_work_year, slicer_work_week, slicer_locations

slicer_work_year, slicer_work_week, slicer_location = global_slicer_data()