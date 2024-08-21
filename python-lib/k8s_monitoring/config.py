import dataiku
from datetime import datetime

# --------------------------------------------------------------------------
# Specific Dataiku variables
client = dataiku.api_client()
instance_info = client.get_instance_info()
data_dir = instance_info.raw["dataDirPath"]
node_name = instance_info.raw["nodeName"]

# Datetime to be used on all the outputs
dt = datetime.utcnow()

# --------------------------------------------------------------------------
# Pod Status Columns
pod_cleansed_cols = [
    'date_time', 'dt_year', 'dt_month', 'dt_day', 'dt_hour', 'dt_minute',
    'dss_node_name', 'dataiku_project_key', 'pod_submitter', 'pod_namespace',
    'pod_exec_type', 'pod_exec_id', 'pod_activity_id', 'pod_job_id', 'pod_full_name',
    'pod_ip', 'pod_phase', 'pod_create_date', 'pod_age_sec',
    'pod_cpu_limit', 'pod_cpu_request', 'pod_cpu_usage', 'pod_cpu_percent',
    'pod_memory_limit', 'pod_memory_request', 'pod_memory_usage', 'pod_memory_percent',
    'k8s_node_name'
]

# --------------------------------------------------------------------------
# Cluster Information
cluster_type = "AWS"
cluster_name = 'fe-sandbox-cluster'

# File Folder save information
folder_conn = 'filesystem_folders'
raw_folder_path = 'incoming'
raw_folder_name = 'k8s_monitoring_raw'
cleanse_folder_name = 'k8s_monitoring_cleanse'
cleanse_folder_path = '' # Leave actually blank unless desired to change path
file_ext = 'csv'

# AWS / EKS Information
aws_region = 'us-west-2'

# GCP / GKE Information
gcp_project_id = 'smazzei'
gcp_zone = 'us-central1-f'

# --------------------------------------------------------------------------
# EOF