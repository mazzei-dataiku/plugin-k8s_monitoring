from k8s_monitoring import config
import dataiku
import pandas as pd
import io  


def get_folder():
    folder = dataiku.Folder(
            lookup=config.folder_id, 
            project_key=dataiku.default_project_key(),
            ignore_flow=True
    )
    return folder


def save_data_folder(dt, name, df, mode=None):
    # Date information -- always pad for time series partitioning
    dt_year  = str(dt.year)
    dt_month = str(f'{dt.month:02d}')
    dt_day   = str(f'{dt.day:02d}')
    
    # Get file save type (CSV | Parquet)
    save_type = config.file_ext
    
    # setup paths
    if mode == "incoming":
        dt_str = dt.strftime("%Y%m%d")
        path   = f'/{mode}/{name}/{dt_year}/{dt_month}/{dt_day}/run_{dt_str}.{save_type}'
    
    # Get folder
    folder = get_folder()
    
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