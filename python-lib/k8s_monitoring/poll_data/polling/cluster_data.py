from k8s_monitoring import config

def get_data(self, dt):
    cluster_type = self.config["cluster_type"]
    
    if cluster_type == "AWS":
        from k8s_monitoring.poll_data.cloud_provider import aws_cluster_data
        df = aws_cluster_data.get_data(self, dt)
        return df
    
    elif cluster_type == "Azure":
        raise Exception("Azure cluster has not been implemented yet.")
    
    elif cluster_type == "GCP":
        rom k8s_monitoring.poll_data.cloud_provider import aws_cluster_data
        df = aws_cluster_data.get_data(self, dt)
        return df
    
    else:
        raise Exception(f"Invalid cluster type: {cluster_type}")
