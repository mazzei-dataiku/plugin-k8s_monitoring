from dataiku.customrecipe import get_input_names_for_role, get_recipe_config, get_output_names_for_role

from k8s_monitoring.cleanse_data import main
from datetime import datetime

input_A_names = get_input_names_for_role('input_folder')
print(f"AHHHHHHHH input_A_names")



dt = datetime.utcnow()
r = main.cleanse_data(dt, "incoming|cluster_data")
r = main.cleanse_data(dt, "incoming|nodegroup_data")
r = main.cleanse_data(dt, "incoming|pod_status")
r = main.cleanse_data(dt, "incoming|nodegroup_status")