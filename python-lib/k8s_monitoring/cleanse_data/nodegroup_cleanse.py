from . import cleansing

import pandas as pd

def cleanse(df):
    # Convert
    df = df.where(pd.notnull(df), None)

    # Cleanse CPU Values
    df['node_cpu_max']      = df['node_cpu_max'].apply(cleansing.cleanse_cpu)
    df['node_cpu_current']  = df['node_cpu_current'].apply(cleansing.cleanse_cpu)
    df['node_cpu_percent']  = df[['node_cpu_max', 'node_cpu_current']].apply(cleansing.compute_percent, axis=1)

    # Cleanse Memory Values
    df['node_memory_max']      = df['node_memory_max'].apply(cleansing.cleanse_memory)
    df['node_memory_current']  = df['node_memory_current'].apply(cleansing.cleanse_memory)
    df['node_memory_percent']  = df[['node_memory_max', 'node_memory_current']].apply(cleansing.compute_percent, axis=1)

    # Cleanse Pods Values
    df['node_pods_percent']  = df[['node_pods_max', 'node_pods_current']].apply(cleansing.compute_percent, axis=1)

    # Re-Order the columns
    c = [
        'date_time',
        'nodegroup_name',
        'k8s_node_name',
        'node_type',
        'node_status',
        'node_phase',
        'node_eks_version',
        'node_create_date',
        'node_age_sec',
        'node_storage_max', 'node_storage_current',
        'node_cpu_max',     'node_cpu_current', 'node_cpu_percent',
        'node_memory_max',  'node_memory_current', 'node_memory_percent',
        'node_pods_max',    'node_pods_current', 'node_pods_percent'
    ]
    df = df[c]

    # Cleanse datatime and add columns
    df["date_time"]        = pd.to_datetime(df["date_time"]).dt.floor("S").dt.tz_convert(tz='UTC')
    df["node_create_date"] = pd.to_datetime(df["node_create_date"]).dt.floor("S").dt.tz_convert(tz='UTC')

    df.insert(1, "dt_minute", df["date_time"].dt.minute)
    df.insert(1, "dt_hour",   df["date_time"].dt.hour)
    df.insert(1, "dt_day",    df["date_time"].dt.day)
    df.insert(1, "dt_month",  df["date_time"].dt.month)
    df.insert(1, "dt_year",   df["date_time"].dt.year)
    
    # Minor Cleanse
    cols = [
        'node_age_sec',
        'node_storage_max', 'node_storage_current',
        'node_cpu_max',     'node_cpu_current',
        'node_memory_max',  'node_memory_current',
        'node_pods_max',    'node_pods_current'
    ]
    for c in cols:
        df[c].fillna(0, inplace=True)
        df[c].replace('None', 0, inplace=True)
        df[c] = df[c].astype('int')
    
    cols = ['node_cpu_percent', 'node_memory_percent', 'node_pods_percent']
    for c in cols:
        df[c].fillna(0, inplace=True)
        df[c].replace('None', 0, inplace=True)
        df[c] = df[c].astype('int')
    
    return df

# EOF