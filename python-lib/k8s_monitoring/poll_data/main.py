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
    
    # Cluster Information
    # name = "cluster_data"
    # cluster_df = cluster_data.get_data(dt, project_id, zone, cluster)
    # helper.save_data_folder(dt, name, cluster_df, mode)
     
    # Nodegroup Information
    # name = "nodegroup_data"
    # nodegroup_df = nodegroup_data.get_data(dt, project_id, zone, cluster)
    # helper.save_data_folder(dt, name, nodegroup_df, mode)
    
    # Pod Status
    name = "pod_status"
    pods_df = pod_status.get_data(dt, cluster, data_dir)
    # helper.save_data_folder(dt, name, pods_df, mode)
    
    # Node Status
    # name = "nodegroup_status"
    # ngs_df = nodegroup_status.get_data(dt, cluster, data_dir, pods_df)
    # helper.save_data_folder(dt, name, ngs_df, mode)
    
    return config.data_dir