#!/usr/bin/python3

# Simple example on how Veeam Backup for Nutanix AHV (aka VBN aka VB) 4.0 public REST API can be used
# Current script builds graph of the average CPU usage during the last 7 days. 

from argparse import ArgumentParser

import io
import pandas as pd
import matplotlib.pyplot as plt

import swagger_client
from vbn_4_client_wrapper import Vbn4RestClient

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username",
        help="username to access backup appliance")
    parser.add_argument("-p", "--password", dest="password", 
        help="password to access backup appliance")
    parser.add_argument("-a", "--address", dest="address", 
        help="address of veeam backup appliance")
    args, unknown = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
        
    vb_rest_client = Vbn4RestClient(f"https://{args.address}", args.username, args.password)

    # Patch module to add Direction and Operation 'enums'.
    swagger_client = Vbn4RestClient.patch_swagger_client_module(swagger_client)

    # You need to skip preloading content, otherwise response will be incorrectly parsed as string
    cpu_usage_response = vb_rest_client.MonitoringApi.monitoring_download_cpu_usage_csv(_preload_content=False)
    
    # Process data to show average for all the available dates. 
    cpu_usage_txt = str(cpu_usage_response.data, 'utf-8')
    buffer = io.StringIO(cpu_usage_txt)
    df = pd.read_csv(filepath_or_buffer = buffer)
    df['Date'] = pd.to_datetime(df['CreationTime'], errors='coerce')
    # We want to take average CPU load for each day. MAX value is not really representative. 
    df_mean = df.groupby([df['Date'].dt.date]).mean().head(7) # Get last 7 days
    
    # Build and show the plot
    cpu_plot = df_mean.plot(kind='bar')
    plt.show()

    # You can do the same with storage and RAM. CPU here is just for an example. 


