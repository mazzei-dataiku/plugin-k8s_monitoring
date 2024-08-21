from k8s_monitoring import config
from . import cleansing

import pandas as pd

def cleanse(df):
    # Remove System Level
    #df = df.loc[(df['pod_namespace'].str.contains("dssns-"))]
    if df.empty:
        return pd.DataFrame(columns=config.pod_cleansed_cols)
    
    # Convert
    df = df.where(pd.notnull(df), None)
    
    # Fill Nulls
    df["pod_activity_id"] = df["pod_activity_id"].fillna(df["pod_exec_id"])
    df["pod_job_id"] = df["pod_job_id"].fillna(df["pod_exec_id"])
    df["pod_ip"].fillna("Pending", inplace=True)
    df["k8s_node_name"].fillna("Pending", inplace=True)
    df["pod_cpu_limit"].fillna(-1, inplace=True)

    # Cleanse CPU Values
    df['pod_cpu_limit']    = df['pod_cpu_limit'].apply(cleansing.cleanse_cpu)
    df['pod_cpu_request']  = df['pod_cpu_request'].apply(cleansing.cleanse_cpu)
    df['pod_cpu_usage']    = df['pod_cpu_usage'].apply(cleansing.cleanse_cpu)
    df['pod_cpu_percent']  = df[['pod_cpu_request', 'pod_cpu_usage']].apply(cleansing.compute_percent, axis=1)

    # Cleanse Memory Values
    df['pod_memory_limit']    = df['pod_memory_limit'].apply(cleansing.cleanse_memory)
    df['pod_memory_request']  = df['pod_memory_request'].apply(cleansing.cleanse_memory)
    df['pod_memory_usage']    = df['pod_memory_usage'].apply(cleansing.cleanse_memory)
    df['pod_memory_percent']  = df[['pod_memory_request', 'pod_memory_usage']].apply(cleansing.compute_percent, axis=1)

    # Re-Order the columns
    column_to_move = df.pop("pod_cpu_percent")
    index = df.columns.get_loc("pod_cpu_usage") + 1
    df.insert(index, "pod_cpu_percent", column_to_move)
    
    column_to_move = df.pop("pod_memory_percent")
    index = df.columns.get_loc("pod_memory_usage") + 1
    df.insert(index, "pod_memory_percent", column_to_move)

    # Cleanse datatime and add columns
    df["date_time"]       = pd.to_datetime(df["date_time"]).dt.floor("S").dt.tz_convert(tz='UTC')
    df["pod_create_date"] = pd.to_datetime(df["pod_create_date"]).dt.floor("S").dt.tz_convert(tz='UTC')

    df.insert(1, "dt_minute", df["date_time"].dt.minute)
    df.insert(1, "dt_hour",   df["date_time"].dt.hour)
    df.insert(1, "dt_day",    df["date_time"].dt.day)
    df.insert(1, "dt_month",  df["date_time"].dt.month)
    df.insert(1, "dt_year",   df["date_time"].dt.year)

    # Minor Clean Up
    df['dataiku_project_key'] = df['dataiku_project_key'].str.upper()

    cols = [
        'pod_age_sec',
        'pod_cpu_limit', 'pod_cpu_request', 'pod_cpu_usage', 
        'pod_memory_limit', 'pod_memory_request', 'pod_memory_usage'
    ]
    for c in cols:
        df[c].fillna(0, inplace=True)
        df[c].replace('None', 0, inplace=True)
        df[c] = df[c].astype('int')
    
    cols = ['pod_cpu_percent', 'pod_memory_percent']
    for c in cols:
        df[c].fillna(0, inplace=True)
        df[c].replace('None', 0, inplace=True)
        df[c] = df[c].astype('float')
    
    # Correct column order just in-case
    df = df[config.pod_cleansed_cols]
    
    return df

# EOF