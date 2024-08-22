import pandas as pd
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

def get_data(self, dt):
    subscription_id = "82852abb-55ae-44d8-9bac-4632a4173215"
    resource_group = 'cbutler-fm-rg'
    cluster_name = 'mazzei-aks'

    credential = AzureCliCredential()
    resouce_client = ResourceManagementClient(credential,subscription_id)
    container_client = ContainerServiceClient(credential,subscription_id)
    resouce_list = resouce_client.resources.list_by_resource_group(resource_group)
    get_aks = container_client.managed_clusters.get(resource_group, cluster_name)

    data = [
        dt, get_aks.as_dict()["location"],
        get_aks.as_dict()["name"], get_aks.as_dict()["power_state"]["code"],
        get_aks.as_dict()["kubernetes_version"], get_aks.as_dict()["current_kubernetes_version"]
    ]

    c = [
        'date_time', 'azure_location', 
        'cluster_name', 'cluster_status',
        'cluster_orig_version', 'cluster_current_version'
    ]
    
    df = pd.DataFrame([data], columns=c)
    return df

# EOF