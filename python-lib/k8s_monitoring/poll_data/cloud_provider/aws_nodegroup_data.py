import pandas as pd
import boto3


def get_data(self, dt):
    aws_region = self.config["aws_region"]
    cluster_name = self.config["cluster_name"]
    
    eks = boto3.client("eks", region_name=aws_region)
    ec2 = boto3.client("ec2", region_name=aws_region)
    
    data = []
    r = eks.list_nodegroups(clusterName=cluster_name)
    for ng in r['nodegroups']:
        try:
            r = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=ng)
        except:
            continue
    
        date_time = dt
        nodegroup_name = ng
        nodegroup_instance_type = r['nodegroup']['instanceTypes']
        nodegroup_AS_enabled = r['nodegroup']['capacityType']
        nodegroup_desired_size = r['nodegroup']['scalingConfig']['desiredSize']
        nodegroup_min_size = r['nodegroup']['scalingConfig']['minSize']
        nodegroup_max_size = r['nodegroup']['scalingConfig']['maxSize']
        instance_type_md = ec2.describe_instance_types(InstanceTypes=nodegroup_instance_type)
        instance_desc = r['nodegroup']['amiType']
        instance_cores = instance_type_md['InstanceTypes'][0]['VCpuInfo']['DefaultCores']
        instance_memory = instance_type_md['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
        print(r)
        
        try:
            gpu_count = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["Count"]
            gpu_cpu = 0
            gpu_memory = instance_type_md["InstanceTypes"][0]["GpuInfo"]["Gpus"][0]["MemoryInfo"]["SizeInMiB"]
        except:
            gpu_count = 0
            gpu_cpu = 0
            gpu_memory = 0
        #instance_price = 1.0080
        #if gpu_count > 0:
        #    instance_price = 0.5260
        
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