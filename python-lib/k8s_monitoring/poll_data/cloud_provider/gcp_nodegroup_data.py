import pandas as pd
from google.cloud import container_v1
from google.cloud import compute

def get_data(self, dt):
    project_id = self.config["gcp_project_id"]
    zone = self.config["gcp_zone"]
    cluster_name = self.config["cluster_name"]
    
    # Make the connection
    client = container_v1.ClusterManagerClient()
    response = client.get_cluster(name=f'projects/{project_id}/locations/{zone}/clusters/{cluster_name}')

    data = []
    for np in response.node_pools:
        date_time = dt
        nodegroup_name = np.name
        nodegroup_instance_type = np.config.machine_type

        nodegroup_AS_enabled = np.autoscaling.enabled
        nodegroup_desired_size = np.initial_node_count
        if nodegroup_AS_enabled:
            nodegroup_min_size = np.autoscaling.min_node_count
            nodegroup_max_size = np.autoscaling.max_node_count
        else:
            nodegroup_min_size = 0
            nodegroup_max_size = 0

        # Build a client to learn more about the machine type
        client = compute.MachineTypesClient()
        request = compute.GetMachineTypeRequest(
            machine_type = nodegroup_instance_type,
            project = project_id,
            zone = zone
        )
        mt_response = client.get(request=request)

        # Parse the mt_response on Machine Type
        instance_desc = mt_response.description
        instance_cores = mt_response.guest_cpus
        instance_memory = mt_response.memory_mb
        gpu_count = 0
        gpu_cpu = 0
        gpu_memory = 0
        try:
            gpu_count = "TBD"
            gpu_cpu = mt_response.gpu_cpu
            gpu_memory = mt_response.gpu_memory
        except:
            pass

        # Estimated costs per hour
        # https://cloud.google.com/compute/all-pricing
        #instance_price = 0.473212

        t = [
            dt,
            nodegroup_name, nodegroup_instance_type,
            nodegroup_AS_enabled, nodegroup_desired_size, nodegroup_min_size, nodegroup_max_size,
            instance_desc, instance_cores, instance_memory, gpu_count, gpu_cpu, gpu_memory
        ]
        data.append(t)

    cols = [
        "date_time",
        "nodegroup_name", "nodegroup_instance_type",
        "nodegroup_AS_enabled", "nodegroup_desired_size", "nodegroup_min_size", "nodegroup_max_size",
        "instance_desc", "instance_cores", "instance_memory", "gpu_count", "gpu_cpu", 'gpu_memory'
    ]

    df = pd.DataFrame(data, columns=cols)
    return df

# EOF