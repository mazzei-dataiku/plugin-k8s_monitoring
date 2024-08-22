from dataiku.runnables import Runnable
from k8s_monitoring.poll_data import main


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        #return self.config["cluster_name"]
        output = main.poll_data(self)
        return output
        