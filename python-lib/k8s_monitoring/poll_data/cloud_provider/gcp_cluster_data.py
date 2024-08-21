import pandas as pd
from google.cloud import container_v1
from googleapiclient import discovery

def get_data(dt, project_id, zone, cluster):
    client = container_v1.ClusterManagerClient()
    service = discovery.build('compute', 'v1')
    response = client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{cluster}')
    data = [
        dt, project_id, zone,
        response.name,
        response.create_time,
        response.status.name,
        response.initial_cluster_version,
        response.current_master_version,
        response.current_node_version,
        response.current_node_count
    ]
    
    c = [
        'date_time', 'project_id', 'zone',
        'cluster_name', 'cluster_create_time', 'cluster_status',
        'cluster_initial_version', 'cluster_current_version', 'cluster_node_version',
        'cluster_node_count'
    ]
    
    df = pd.DataFrame([data], columns=c)
    return df

# EOF