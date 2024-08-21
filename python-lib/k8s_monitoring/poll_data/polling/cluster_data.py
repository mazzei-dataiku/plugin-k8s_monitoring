from k8s_monitoring.polling import config

def get_data(dt):
    cluster_name = config.cluster_name
    
    project_id = config.project_id
    zone = config.zone