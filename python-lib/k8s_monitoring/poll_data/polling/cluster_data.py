from k8s_monitoring.polling import config

def get_data(dt):
    cluster_type = config.cluster_type
    
    if cluster_type == "AWS":
        from k8s_monitoring.poll_data.cloud_provider import get_data
        df = get_data(dt)
        return df
    
    elif cluster_type == "Azure":
        return 123
    elif cluster_type == "GCP":
        return 123
    else:
        raise Exception(f"Invalid cluster type: {cluster_type}")
