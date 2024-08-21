import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from datetime import datetime

from k8s_monitoring.modules import pod_cleanse
from k8s_monitoring.modules import nodegroup_cleanse


def cleanse_data(partition):
    # get some values
    mode, data = partition.split("|")
    k8s_monitoring = dataiku.Folder("CjgexdB8", ignore_flow=True)
    k8s_monitoring_cleansed = dataiku.Folder("7HBKWZDX")

    # Date time stuff
    dt = datetime.utcnow()
    dt_year  = str(dt.year)
    dt_month = str(f'{dt.month:02d}')
    dt_day   = str(f'{dt.day:02d}')

    # Get current list of files
    l1 = k8s_monitoring.list_paths_in_partition(partition=partition)

    # Cleanse
    for csv in l1:
        # Read in the base data
        with k8s_monitoring.get_download_stream(path=csv) as stream:
            df = pd.read_csv(stream)

        # Cleanse
        if data == "pod_status":
            new_df = pod_cleanse.cleanse(df)
        elif data == "nodegroup_status":
            new_df = nodegroup_cleanse.cleanse(df)
        else:
            new_df = df.copy(deep=True)

        # Save new data to output folder
        new_csv = csv.replace("/incoming", "")
        with k8s_monitoring_cleansed.get_writer(new_csv) as writer:
            writer.write(new_df.to_csv(index=False).encode("utf-8"))

        # move the original if its not the current day
        today = f"/incoming/{data}/{dt_year}/{dt_month}/{dt_day}/run_{dt_year}{dt_month}{dt_day}.csv"
        if csv == today:
            continue
        ## Move / Save to cold storage
        cold_csv = csv.replace("incoming", "cold")
        with k8s_monitoring.get_writer(cold_csv) as writer:
            writer.write(df.to_csv(index=False).encode("utf-8"))
        ## Delete the original
        k8s_monitoring.delete_path(path=csv)
    return True

def run():
    k8s_monitoring = dataiku.Folder("CjgexdB8", ignore_flow=True)

    k8s_monitoring_cleansed = dataiku.Folder("7HBKWZDX")

    dt = datetime.utcnow()
    dt_year  = str(dt.year)
    dt_month = str(f'{dt.month:02d}')
    dt_day   = str(f'{dt.day:02d}')

    cleanse_data("incoming|cluster_data")
    cleanse_data("incoming|nodegroup_data")
    cleanse_data("incoming|pod_status")
    cleanse_data("incoming|nodegroup_status")
    
    return "Cleansed"