def get_data(self, dt):
    cluster_type = self.config["cluster_type"]
    
    if cluster_type == "AWS":
        from k8s_monitoring.poll_data.cloud_provider import aws_nodegroup_data
        df = aws_nodegroup_data.get_data(self, dt)
        return df
    
    elif cluster_type == "AZURE":
        from k8s_monitoring.poll_data.cloud_provider import azure_nodegroup_data
        df = azure_nodegroup_data.get_data(self, dt)
        return df
    
    elif cluster_type == "GCP":
        from k8s_monitoring.poll_data.cloud_provider import gcp_nodegroup_data
        df = gcp_nodegroup_data.get_data(self, dt)
        return df
    
    else:
        raise Exception(f"Invalid cluster type: {cluster_type}")
