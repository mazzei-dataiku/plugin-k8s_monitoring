from k8s_monitoring.polling import config

def get_data(dt):
    cluster_type = config.cluster_type
    cluster_name = config.cluster_name
    
    if cluster_type == "AWS":
        from k8s_monitoring.poll_data.cloud_provider import get_data
        df = get_data(dt)
    elif cluster_type == "Azure":
        123
    elif cluster_type == "GCP":
        123
    else:
        raise Exception(f"Invalid cluster type: {cluster_type}")
