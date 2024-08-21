from .helper import load_yaml

import pandas as pd
import boto3


def get_data(NOW, instance_name):
    # Build Cluster Data Frame
    k8s_yaml = load_yaml(instance_name)
    cluster_name = k8s_yaml['metadata']['name']
    
    eks = boto3.client("eks")
    r = eks.describe_cluster(name=cluster_name)
    cluster_create_date = r['cluster']['createdAt'],
    cluster_version = r['cluster']['version'],
    cluster_platform_version = r['cluster']['platformVersion']

    c = [
        [
            NOW,
            cluster_name,
            cluster_create_date[0],
            cluster_version[0],
            cluster_platform_version
        ]
    ]

    columns = [
        'date_time',
        'cluster_name',
        'cluster_create_date',
        'cluster_version',
        'cluster_plat_version'
    ]
    clusters_df = pd.DataFrame(c, columns=columns)
    
    # Forcing some DT stuff
    clusters_df['date_time'] = clusters_df['date_time'].dt.tz_localize(None)
    clusters_df['date_time'] = clusters_df['date_time'].dt.tz_localize('UTC')

    clusters_df['cluster_create_date'] = clusters_df['cluster_create_date'].dt.tz_localize(None)
    clusters_df['cluster_create_date'] = clusters_df['cluster_create_date'].dt.tz_localize('UTC')
    
    # Forcing some other items
    c = list(clusters_df.columns)
    c.remove('date_time')
    c.remove('cluster_create_date')
    clusters_df[c] = clusters_df[c].astype('str')

    return clusters_df