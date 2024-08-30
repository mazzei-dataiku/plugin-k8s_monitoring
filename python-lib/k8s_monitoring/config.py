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
    'dss_node_name', 'dataiku_project_key', 'pod_submitter', 'pod_namespace',  'pod_full_name',
    'pod_exec_type', 'pod_exec_id', 'pod_activity_id', 'pod_job_id','pod_webapp_id',
    'pod_analysis_id', 'pod_mltask_id', 'pod_mltask_session_id',
    'pod_apideployer_infra_id', 'pod_apideployer_serv_id', 'pod_apideployer_depl_id',
    
    
    'pod_ip', 'pod_phase', 'pod_create_date', 'pod_age_sec',
    'pod_cpu_limit', 'pod_cpu_request', 'pod_cpu_usage', 'pod_cpu_percent',
    'pod_memory_limit', 'pod_memory_request', 'pod_memory_usage', 'pod_memory_percent',
    'k8s_node_name'
]

# --------------------------------------------------------------------------
# File Folder save information
raw_folder_path = 'incoming'
file_ext = 'csv'
cleanse_folder_path = ''

# --------------------------------------------------------------------------
# EOF