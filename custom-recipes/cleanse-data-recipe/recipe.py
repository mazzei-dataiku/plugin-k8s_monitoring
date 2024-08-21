from k8s_monitoring.cleanse_data import main
from datetime import datetime


dt = datetime.utcnow()
r = main.cleanse_data(dt, "incoming|cluster_data")
r = main.cleanse_data(dt, "incoming|nodegroup_data")
r = main.cleanse_data(dt, "incoming|pod_status")
r = main.cleanse_data(dt, "incoming|nodegroup_status")