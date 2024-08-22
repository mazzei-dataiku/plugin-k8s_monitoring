from k8s_monitoring import config

import pandas as pd
import datetime
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config

def get_data(self, dt, pods_df):
    cluster_name = self.config["cluster_name"]
    data_dir = config.data_dir
    
    kube_config = f"{data_dir}/clusters/{cluster_name}/exec/kube_config"
    k8s_config.load_kube_config(config_file=kube_config)

    v1 = k8s_client.CoreV1Api()
    ret = v1.list_node()
    l =[]

    for i in ret.items:
        t = []
        # Current UTC Time
        t.append(dt)

        # Node Information
        t.append(i.metadata.labels['kubernetes.io/hostname'])
        t.append(i.metadata.name)
        #t.append(i.metadata.labels['dss_usage'])
        t.append(i.metadata.labels['beta.kubernetes.io/instance-type'])
        t.append(i.status.conditions[-1].status)
        t.append(i.status.phase)
        t.append(i.status.node_info.kubelet_version)
        t.append(i.metadata.creation_timestamp)
        t.append(datetime.datetime.now(tz=datetime.timezone.utc) - i.metadata.creation_timestamp)
        t.append(i.status.allocatable['ephemeral-storage'])
        t.append(0)
        t.append(i.status.allocatable['cpu'])
        t.append(0)
        t.append(i.status.allocatable['memory'])
        t.append(0)
        t.append(i.status.allocatable['pods'])
        t.append(0)
        l.append(t)

    #   Build Data Frame
    columns = [
        'date_time',
        'nodegroup_name',
        'k8s_node_name',
        'node_type',
        'node_status',
        'node_phase',
        'node_eks_version',
        'node_create_date',
        'node_age_sec',
        'node_storage_max', 'node_storage_current',
        'node_cpu_max',     'node_cpu_current',
        'node_memory_max',  'node_memory_current',
        'node_pods_max',    'node_pods_current'
    ]

    nodes_df = pd.DataFrame(l, columns=columns)

    #   Add in node Metrics
    cust = k8s_client.CustomObjectsApi()
    api_cust = cust.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', 'nodes') # All node metrics

    for i in api_cust['items']:
        nname = i['metadata']['name']

        # CPU Percent
        ncpu = i['usage']['cpu']
        nodes_df.loc[nodes_df['k8s_node_name'] == nname, 'node_cpu_current'] = ncpu

        # Memory Percent
        nmem = i['usage']['memory']
        nodes_df.loc[nodes_df['k8s_node_name'] == nname, 'node_memory_current'] = nmem

    nodes_df['node_age_sec'] = nodes_df.node_age_sec.dt.seconds
    groups = pods_df.groupby(by='k8s_node_name')
    for i, g in groups:
        count = len(g.loc[g["pod_namespace"] != 'kube-system'])
        nodes_df.loc[nodes_df['k8s_node_name'] == i, 'node_pods_current'] = count

    # Forcing some DT stuff
    nodes_df['date_time'] = nodes_df['date_time'].dt.tz_localize(None)
    nodes_df['date_time'] = nodes_df['date_time'].dt.tz_localize('UTC')

    nodes_df['node_create_date'] = nodes_df['node_create_date'].dt.tz_localize(None)
    nodes_df['node_create_date'] = nodes_df['node_create_date'].dt.tz_localize('UTC')

    # Forcing some other items
    c = list(nodes_df.columns)
    c.remove('date_time')
    c.remove('node_create_date')
    nodes_df[c] = nodes_df[c].astype('str')


    return nodes_df

# EOF