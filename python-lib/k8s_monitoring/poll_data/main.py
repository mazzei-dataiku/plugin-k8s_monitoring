import pandas as pd
import datetime
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config

def poll_data():
    # Load config variables
    p = "/data/dataiku/dss_data/clusters/fe-sandbox-cluster/exec/kube_config"
    try:
        k8s_config.load_kube_config(config_file=kube_config)
    except Exception as e:
        return e
    return "I can read"