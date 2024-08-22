import pandas as pd
import boto3


def get_data(self, dt):
    cluster_name = self.config["cluster_name"]
    aws_region = self.config["aws_region"]
    
    eks = boto3.client("eks", region_name=aws_region)
    r = eks.describe_cluster(name=cluster_name)
    data = [
            dt, aws_region, cluster_name,
            r['cluster']['createdAt'],
            r["cluster"]["status"],
            r['cluster']['version'],
            r['cluster']['platformVersion']
    ]
    columns = [
        'date_time', 'aws_region', 'cluster_name',
        'cluster_create_date', 'cluster_status', 'cluster_version', 'cluster_plat_version'
    ]
    df = pd.DataFrame([data], columns=columns)
    return df