from k8s_monitoring import config

def poll_data():
    # Load config variables
    dt = config.dt
    data_dir = config.data_dir
    project_id = config.project_id
    zone = config.zone
    cluster = config.cluster
    
    # mode type
    mode = "incoming"
    
    return config.data_dir