from k8s_monitoring import config

import pandas as pd
import datetime
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config


def get_data(self, dt):
    cluster_name = self.config["cluster_name"]
    data_dir = config.data_dir
    
    kube_config = f"{data_dir}/clusters/{cluster_name}/exec/kube_config"
    k8s_config.load_kube_config(config_file=kube_config)

    v1 = k8s_client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    l =[]

    for i in ret.items:
        t = []
        # Current UTC Time
        t.append(dt)

        # DSS Project Key
        dss_node_name   = None
        project_key     = None
        pod_submitter   = None
        pod_exec_type   = None
        pod_exec_id     = None
        pod_activity_id = None
        pod_job_id      = None
        labels = i.metadata.labels
        if labels:
            dss_node_name   = labels.get('dataiku.com/dku-node-id',        None) # nodeid must be set in DATA_DIR/install.ini
            dss_install_id  = labels.get('dataiku.com/dku-install-id',     None) # nodeid must be set in DATA_DIR/install.ini
            project_key     = labels.get('dataiku.com/dku-project-key',    None)
            pod_submitter   = labels.get('dataiku.com/dku-exec-submitter', None)
            pod_exec_type   = labels.get('dataiku.com/dku-execution-type', None)
            pod_exec_id     = labels.get('dataiku.com/dku-execution-id',   None)
            pod_activity_id = labels.get('dataiku.com/dku-activity-id',    None)
            pod_job_id      = labels.get('dataiku.com/dku-job-id',         None)

        t.append(dss_node_name)
        t.append(project_key)
        t.append(pod_submitter)
        t.append(i.metadata.namespace)
        t.append(pod_exec_type)
        t.append(pod_exec_id)
        t.append(pod_activity_id)
        t.append(pod_job_id)
        t.append(i.metadata.name)
        t.append(i.status.pod_ip)
        t.append(i.status.phase)
        t.append(i.metadata.creation_timestamp)
        t.append(datetime.datetime.now(tz=datetime.timezone.utc) - i.metadata.creation_timestamp)

        # Limits
        limit_cpu = None
        limit_memory = None
        if i.spec.containers[0].resources.limits:
            if 'cpu' in i.spec.containers[0].resources.limits.keys():
                limit_cpu = i.spec.containers[0].resources.limits['cpu']
            if 'memory' in i.spec.containers[0].resources.limits.keys():
                limit_memory = i.spec.containers[0].resources.limits['memory']


        # Requests
        requests_cpu = None
        requests_memory = None
        if i.spec.containers[0].resources.requests:
            if 'cpu' in i.spec.containers[0].resources.requests.keys():
                requests_cpu = i.spec.containers[0].resources.requests['cpu']
            if 'memory' in i.spec.containers[0].resources.requests.keys():
                requests_memory = i.spec.containers[0].resources.requests['memory']

        # Performance Numbers
        t.append(limit_cpu)
        t.append(requests_cpu)
        t.append("0")
        t.append(limit_memory)
        t.append(requests_memory)
        t.append("0")
        t.append(i.spec.node_name)
        l.append(t)
    
    #   Build Data Frame
    columns=[
        'date_time',
        'dss_node_name', 'dataiku_project_key', 
        'pod_submitter', 'pod_namespace',
        'pod_exec_type', 'pod_exec_id', 'pod_activity_id', 'pod_job_id',
        'pod_full_name',
        'pod_ip',
        'pod_phase',
        'pod_create_date',
        'pod_age_sec',
        'pod_cpu_limit',    'pod_cpu_request',    'pod_cpu_usage',
        'pod_memory_limit', 'pod_memory_request', 'pod_memory_usage',
        'k8s_node_name'
    ]

    pods_df = pd.DataFrame(l, columns=columns)
    
    #   Add in pod Metrics
    cust_objs = k8s_client.CustomObjectsApi()
    list_cluster_cust_objs = cust_objs.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', 'pods') # All Pod Metrics

    for i in list_cluster_cust_objs['items']:
        pname = i['metadata']['name']

        # CPU Usage
        if i['containers']:
            pcpu = i['containers'][0]['usage']['cpu']
            pods_df.loc[pods_df['pod_full_name'] == pname, 'pod_cpu_usage'] = pcpu

        # Memory Usage
        if i['containers']:
            pmem = i['containers'][0]['usage']['memory']
            pods_df.loc[pods_df['pod_full_name'] == pname, 'pod_memory_usage'] = pmem

    pods_df['pod_age_sec'] = pods_df.pod_age_sec.dt.seconds
    
    # Forcing some DT stuff
    pods_df['date_time'] = pods_df['date_time'].dt.tz_localize(None)
    pods_df['date_time'] = pods_df['date_time'].dt.tz_localize('UTC')

    pods_df['pod_create_date'] = pods_df['pod_create_date'].dt.tz_localize(None)
    pods_df['pod_create_date'] = pods_df['pod_create_date'].dt.tz_localize('UTC')
    
    return pods_df

# EOF