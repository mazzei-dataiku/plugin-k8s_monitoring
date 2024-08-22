from dataiku.runnables import Runnable

from k8s_monitoring import config
from k8s_monitoring import helper

from k8s_monitoring.poll_data.polling import cluster_data
from k8s_monitoring.poll_data.polling import nodegroup_data
from k8s_monitoring.poll_data.polling import pod_status
from k8s_monitoring.poll_data.polling import nodegroup_status


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Load config variables
        dt = config.dt
        folder_name = self.config["raw_folder_name"]
        folder_path = self.config["aw_folder_path"]

        # Cluster Information
        name = "cluster_data"
        cluster_df = cluster_data.get_data(self, dt)
        helper.save_data_folder(dt, name, cluster_df, folder_name, folder_path)

        # Nodegroup Information
        name = "nodegroup_data"
        nodegroup_df = nodegroup_data.get_data(dt)
        helper.save_data_folder(dt, name, nodegroup_df, folder_name, folder_path)

        # Pod Status
        name = "pod_status"
        pods_df = pod_status.get_data(dt)
        helper.save_data_folder(dt, name, pods_df, folder_name, folder_path)   

        # Node Status
        name = "nodegroup_status"
        ngs_df = nodegroup_status.get_data(dt, pods_df)
        helper.save_data_folder(dt, name, ngs_df, folder_name, folder_path)

        return "FINISH"
        