from dataiku.runnables import Runnable
from k8s_monitoring.cleanse_data import main


class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        k8s_monitoring = dataiku.Folder("CjgexdB8", ignore_flow=True)
        k8s_monitoring_cleansed = dataiku.Folder("7HBKWZDX")

        dt = datetime.utcnow()
        dt_year  = str(dt.year)
        dt_month = str(f'{dt.month:02d}')
        dt_day   = str(f'{dt.day:02d}')

        main.cleanse_data("incoming|cluster_data")
        main.cleanse_data("incoming|nodegroup_data")
        main.cleanse_data("incoming|pod_status")
        main.cleanse_data("incoming|nodegroup_status")
        return output
        