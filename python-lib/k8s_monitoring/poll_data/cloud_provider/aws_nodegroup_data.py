from .helper import load_yaml

import pandas as pd
import boto3


def get_data(NOW, instance_name):
    # Build Node Group Data Frame
    # https://instances.vantage.sh/

    k8s_yaml = load_yaml(instance_name)
    ec2 = boto3.client("ec2")
    ng = []
    for i in k8s_yaml['nodeGroups']:
        nodegroup_name = i['name']
        min_size = i['minSize']
        max_size = i['maxSize']
        desired_size = i['desiredCapacity']
        instance_type = i['instanceType']

        instance_type_md = ec2.describe_instance_types(InstanceTypes=[instance_type])
        instance_cores = instance_type_md['InstanceTypes'][0]['VCpuInfo']['DefaultCores']
        instance_vcores = instance_type_md['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
        instance_memory = instance_type_md['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
        try:
            gpu_count = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["Count"]
            gpu_memory = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["MemoryInfo"]["SizeInMiB"]
        except:
            gpu_count = 0
            gpu_memory = 0
        instance_price = 1.0080
        if gpu_count > 0:
            instance_price = 0.5260

        ng.append([
            NOW,
            nodegroup_name, min_size, max_size, desired_size,
            instance_type, instance_price, instance_cores, instance_vcores, instance_memory, 
            gpu_count, gpu_memory
        ])

    columns = [
        'date_time',
        'nodegroup_name',
        'nodegroup_min_size',
        'nodegroup_max_size',
        'nodegroup_desired_size',
        'nodegroup_instance_type',
        'instance_price',
        'instance_cores',
        'instance_vcores',
        'instance_memory',
        'gpu_count',
        'gpu_memory',
    ]

    nodegroup_df = pd.DataFrame(ng, columns=columns)
    
    # Forcing some DT stuff
    nodegroup_df['date_time'] = nodegroup_df['date_time'].dt.tz_localize(None)
    nodegroup_df['date_time'] = nodegroup_df['date_time'].dt.tz_localize('UTC')
    
    # Forcing some other items
    c = list(nodegroup_df.columns)
    c.remove('date_time')
    nodegroup_df[c] = nodegroup_df[c].astype('str')
    
    return nodegroup_df