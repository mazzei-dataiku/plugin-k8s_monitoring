from k8s_monitoring.poll_data import config
from k8s_monitoring.poll_data import helper

#from k8s_monitoring.poll_data import cluster_data
#from k8s_monitoring.poll_data import nodegroup_data
from k8s_monitoring.poll_data.polling import pod_status
from k8s_monitoring.poll_data.polling import nodegroup_status


def poll_data():
    # Load config variables
    dt = config.dt
    folder_type = config.folder_type
    
    # Cluster Information
    # name = "cluster_data"
    # cluster_df = cluster_data.get_data(dt)
    # helper.save_data_folder(dt, name, cluster_df, folder_type)
     
    # Nodegroup Information
    # name = "nodegroup_data"
    # nodegroup_df = nodegroup_data.get_data(dt, cluster_name)
    # helper.save_data_folder(dt, name, nodegroup_df, folder_type)
    
    # Pod Status
    name = "pod_status"
    pods_df = pod_status.get_data(dt, cluster_name, data_dir)
    helper.save_data_folder(dt, name, pods_df, folder_type)    
    
    # Node Status
    name = "nodegroup_status"
    ngs_df = nodegroup_status.get_data(dt, cluster_name, data_dir, pods_df)
    helper.save_data_folder(dt, name, ngs_df, folder_type)
    
    return "FINISH"