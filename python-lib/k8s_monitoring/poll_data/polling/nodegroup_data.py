def get_data(self, dt):
    cluster_type = self.config["cluster_type"]
    
    if cluster_type == "AWS":
        from k8s_monitoring.poll_data.cloud_provider import aws_nodegroup_data
        df = aws_nodegroup_data.get_data(self, dt)
        return df
    
    elif cluster_type == "Azure":
        raise Exception("Azure cluster has not been implemented yet.")
    
    elif cluster_type == "GCP":
        return 123
    
    else:
        raise Exception(f"Invalid cluster type: {cluster_type}")
