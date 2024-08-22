import pandas as pd
from azure.identity import AzureCliCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.compute import ComputeManagementClient


def get_data(self, dt):
    subscription_id = "82852abb-55ae-44d8-9bac-4632a4173215"
    resource_group = 'cbutler-fm-rg'
    cluster_name = 'mazzei-aks'

    credential = AzureCliCredential()
    container_client = ContainerServiceClient(credential,subscription_id)
    get_aks = container_client.managed_clusters.get(resource_group, cluster_name)
    location = get_aks.as_dict()["location"]

    data = []
    for ng in get_aks.as_dict()["agent_pool_profiles"]:
        nodegroup_name = ng["name"]
        nodegroup_instance_type = ng["vm_size"]
        nodegroup_AS_enabled = ng["enable_auto_scaling"]
        nodegroup_min_size = ng["min_count"]
        nodegroup_max_size = ng["max_count"]
        instance_desc = ng["node_image_version"]

        compute_client = ComputeManagementClient(credential, subscription_id)
        vmSizes = compute_client.virtual_machine_sizes.list(location)
        for vm in vmSizes:
            if vm.as_dict()["name"] == nodegroup_instance_type:
                instance_cores = vm.as_dict().get("number_of_cores", 0)
                instance_memory = vm.as_dict().get("memory_in_mb", 0)
                gpu_count = vm.as_dict().get("gpu_count", 0)
                gpu_cpu = vm.as_dict().get("gpu_cores", 0)
                gpu_memory = vm.as_dict().get("gpu_mem", 0)
        
        t = [
            dt, 
            nodegroup_name, nodegroup_instance_type,
            nodegroup_AS_enabled, nodegroup_min_size, nodegroup_max_size,
            instance_desc, instance_cores, instance_memory, gpu_count, gpu_cpu, gpu_memory
        ]
        data.append(t)

    cols = [
        "date_time",
        "nodegroup_name", "nodegroup_instance_type",
        "nodegroup_AS_enabled", "nodegroup_min_size", "nodegroup_max_size",
        "instance_desc", "instance_cores", "instance_memory", "gpu_count", "gpu_cpu", 'gpu_memory'
    ]

    df = pd.DataFrame(data, columns=cols)
    return df