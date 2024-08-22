import pandas as pd
from azure.identity import AzureCliCredential
from azure.mgmt.containerservice import ContainerServiceClient

def get_data(self, dt):
    subscription_id = self.config["azure_sub_id"]
    resource_group = self.config["azure_resource_grp"]
    cluster_name = self.config["cluster_name"]

    credential = AzureCliCredential()
    container_client = ContainerServiceClient(credential,subscription_id)
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