import pandas as pd
import boto3


def get_data(self, dt):
    aws_region = self.config["aws_region"]
    cluster_name = self.config["cluster_name"]
    
    eks = boto3.client("eks", region_name=aws_region)
    ec2 = boto3.client("ec2", region_name=aws_region)
    
    data = []
    ngs = eks.list_nodegroups(clusterName=cluster_name)["nodegroups"]
    for ng in ngs:
        try:
            r = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=ng)
        except:
            continue
    
        date_time = dt
        nodegroup_name = ng
        ng_info = r['nodegroup']
        nodegroup_instance_type = ng_info.get('instanceTypes', None)
        nodegroup_AS_enabled = ng_info.get('capacityType', None)
        nodegroup_desired_size = ng_info.get('scalingConfig', None).get('desiredSize', 0)
        nodegroup_min_size = ng_info.get('scalingConfig', None).get('minSize', 0)
        nodegroup_max_size = ng_info.get('scalingConfig', None).get('maxSize', 0)
        instance_desc = ng_info.get('amiType']
        if nodegroup_instance_type:
            instance_type_md = ec2.describe_instance_types(InstanceTypes=nodegroup_instance_type)
            instance_cores = instance_type_md['InstanceTypes'][0]['VCpuInfo']['DefaultCores']
            instance_memory = instance_type_md['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
            try:
                gpu_count = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["Count"]
                gpu_cpu = 0
                gpu_memory = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["MemoryInfo"]["SizeInMiB"]
            except:
                gpu_count = 0
                gpu_cpu = 0
                gpu_memory = 0
        else:
            instance_cores = 0
            instance_memory = 0
            gpu_count = 0
            gpu_cpu = 0
            gpu_memory = 0
        
        # Get all the temp values
        t = [
            dt,
            nodegroup_name, nodegroup_instance_type,
            nodegroup_AS_enabled, nodegroup_desired_size, nodegroup_min_size, nodegroup_max_size,
            instance_desc, instance_cores, instance_memory, gpu_count, gpu_cpu, gpu_memory
        ]
        
        # Add to the main data list
        data.append(t)
    
    # Build the Dataframe
    cols = [
        "date_time",
        "nodegroup_name", "nodegroup_instance_type",
        "nodegroup_AS_enabled", "nodegroup_desired_size", "nodegroup_min_size", "nodegroup_max_size",
        "instance_desc", "instance_cores", "instance_memory", "gpu_count", "gpu_cpu", 'gpu_memory'
    ]
    df = pd.DataFrame(data, columns=cols)
    return df