from k8s_monitoring import config
import dataiku
import pandas as pd
import io  


def get_folder(self):
    client = dataiku.api_client()
    project = client.get_default_project()
    folder = dataiku.Folder(lookup=self.config["folder_name"], project_key=dataiku.default_project_key(), ignore_flow=True)
    try:
        folder.get_id()
    except:
        folder_handle = project.create_managed_folder(name=elf.config["folder_name"], connection_name=celf.config["folder_conn"])
        folder = dataiku.Folder(lookup=folder_name, ignore_flow=True, project_key=dataiku.default_project_key())
    return folder


def save_data_folder(self, dt, name, df:
    # Date information -- always pad for time series partitioning
    dt_year  = str(dt.year)
    dt_month = str(f'{dt.month:02d}')
    dt_day   = str(f'{dt.day:02d}')
    
    # Get file save type (CSV | Parquet)
    save_type = config.file_ext
    
    # setup paths
    if folder_path == "incoming":
        dt_str = dt.strftime("%Y%m%d")
        path   = f'/{folder_path}/{name}/{dt_year}/{dt_month}/{dt_day}/run_{dt_str}.{save_type}'
    
    # Get folder
    folder = get_folder(self)
    
    # We want to append to the daily log
    try:
        with folder.get_download_stream(path) as reader:
            mdf = pd.read_csv(reader)
    except:
        mdf = pd.DataFrame()
        
    mdf = pd.concat([mdf,df], ignore_index=True)
    
    with folder.get_writer(path) as writer:
        writer.write(mdf.to_csv(index=False).encode("utf-8"))
    return

# EOF