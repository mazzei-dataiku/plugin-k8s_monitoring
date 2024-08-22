# Kubernetes Monitoring Plugin

- Author: Stephen Mazzei
- Organization: Dataiku
- Last Update: 2024-08-22

## Description

- This plugin contains 2 key components:
    - K8S Poll-Data: This is the macro that runs all the Cloud Provider utilities and Kubernetes API to gather all the raw metrics (Required)
    - Cleanse K8S Data: This is the python recipe that cleans the base data into a cleanse state (Not Required)

## How To

### Poll Data

1. Download/Install the plugin
1. Create a new Dataiku Project (Code is written for UIF enabled or disabled)
1. Create a new scenario
    1. Name = "Poll K8S Data"
    1. Trigger = Time-based, every 5 minutes
    1. Steps = Execute Macro, "Poll K8S Data"
        - Cluster Name
        - Cluster Type
        - Cloud Provider Information
        - Folder Connection Type (Local/Cloud)
        - Folder Name
        [Example](./.images/macro_scenario.png)
    1. Run Scenario
1. Update the new folder in the flow for partitioning
    1. Add 2 "Dimensions" partions
    [Example](./.images/partitioning.png)

### Cleanse Data

1. From Recipe dropdown in flow, select "Kubernetes Monitoring"
1. Select Cleanse K8S Data
1. Select the Raw folder for input, and create a new folder for output
1. **NOTE** Under the "Advanced Tab" you may need to disable "Container Configuration" depending on the DSS Setup
1. Run