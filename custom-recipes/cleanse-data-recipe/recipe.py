from dataiku.customrecipe import get_input_names_for_role, get_recipe_config, get_output_names_for_role

from k8s_monitoring.cleanse_data import main
from datetime import datetime

input_folder = get_input_names_for_role('input_folder')
output_folder = get_input_names_for_role('input_folder')



dt = datetime.utcnow()
r = main.cleanse_data(dt, input_folder, output_folder, "incoming|cluster_data")
r = main.cleanse_data(dt, input_folder, output_folder, "incoming|nodegroup_data")
r = main.cleanse_data(dt, input_folder, output_folder, "incoming|pod_status")
r = main.cleanse_data(dt, input_folder, output_folder, "incoming|nodegroup_status")