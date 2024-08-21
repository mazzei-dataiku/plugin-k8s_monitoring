from k8s_monitoring import helper
from k8s_monitoring.cleanse_data import pod_cleanse
from k8s_monitoring.cleanse_data import nodegroup_cleanse

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from datetime import datetime


def cleanse_data(partition):
    # get some values
    mode, data = partition.split("|")
    raw_folder = folder = get_folder(config.raw_folder_name)
    cleansed_folder = folder = get_folder(config.cleanse_folder_name)

    # Date time stuff
    dt = datetime.utcnow()
    dt_year  = str(dt.year)
    dt_month = str(f'{dt.month:02d}')
    dt_day   = str(f'{dt.day:02d}')

    # Get current list of files
    l1 = raw_folder.list_paths_in_partition(partition=partition)

    # Cleanse
    for csv in l1:
        # Read in the base data
        with raw_folder.get_download_stream(path=csv) as stream:
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
        with cleansed_folder.get_writer(new_csv) as writer:
            writer.write(new_df.to_csv(index=False).encode("utf-8"))

        # move the original if its not the current day
        today = f"/incoming/{data}/{dt_year}/{dt_month}/{dt_day}/run_{dt_year}{dt_month}{dt_day}.csv"
        if csv == today:
            continue
        
        ## Move / Save to cold storage
        cold_csv = csv.replace("incoming", "cold")
        with raw_folder.get_writer(cold_csv) as writer:
            writer.write(df.to_csv(index=False).encode("utf-8"))
        
        ## Delete the original
        raw_folder.delete_path(path=csv)
    return True

# EOF