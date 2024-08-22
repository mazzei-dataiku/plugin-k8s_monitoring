from dataiku.customrecipe import get_input_names_for_role, get_recipe_config, get_output_names_for_role

from k8s_monitoring import config
from k8s_monitoring import helper

from k8s_monitoring.cleanse_data import pod_cleanse
from k8s_monitoring.cleanse_data import nodegroup_cleanse

from datetime import datetime
import pandas as pd

def cleanse_data(dt, input_folder, output_folder, partition):
    # get some values
    mode, data = partition.split("|")
    raw_folder = helper.get_folder(config.raw_folder_name)
    cleansed_folder = helper.get_folder(config.cleanse_folder_name)
    raw_folder_path = config.raw_folder_path

    # Date time stuff
    
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
        new_csv = csv.replace(f"/{raw_folder_path}", "")
        with cleansed_folder.get_writer(new_csv) as writer:
            writer.write(new_df.to_csv(index=False).encode("utf-8"))

        # move the original if its not the current day
        today = f"/{raw_folder_path}/{data}/{dt_year}/{dt_month}/{dt_day}/run_{dt_year}{dt_month}{dt_day}.csv"
        if csv == today:
            #raise Exception(f"Don't remove today")
            continue
        
        ## Move / Save to cold storage
        cold_csv = csv.replace(f"{raw_folder_path}", "cold")
        with raw_folder.get_writer(cold_csv) as writer:
            writer.write(df.to_csv(index=False).encode("utf-8"))
        
        ## Delete the original
        raw_folder.delete_path(path=csv)
    
    return True






input_folder = get_input_names_for_role('input_folder')
output_folder = get_input_names_for_role('input_folder')



dt = datetime.utcnow()
r = cleanse_data(dt, input_folder, output_folder, "incoming|cluster_data")
r = cleanse_data(dt, input_folder, output_folder, "incoming|nodegroup_data")
r = cleanse_data(dt, input_folder, output_folder, "incoming|pod_status")
r = cleanse_data(dt, input_folder, output_folder, "incoming|nodegroup_status")

# EOF