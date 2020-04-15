#Imports
import requests
import pandas as pd
import random
import io
import matplotlib.pyplot as plt
import shutil
import data_miner
import data_cleaner as cleaner
import time
import asyncio


""" 
Universe Miner is built ontop of data miner and used for mining multiple data sources

Example how how to use:

1) Ensure Data Miner module works and configured with the right api key

2)  builder = ub.UniverseBuilder("resources/ftsecodes.txt")
    builder.build_universe()

3) Current limitation is only 5 requests per 5 minutes

# Build's a universe from: CSV's in directory or downloads CSV"s 
# Universe can either be a list of dataframes or a single dataframe

    """
# Constants
# IP_ADDRESS = ['140.82.59.209:8080','159.8.114.37:8123','159.138.1.185:80','159.138.1.185:443','159.89.128.93:8080','159.203.44.177:3128','165.98.139.26:8080','168.131.152.107:3128','169.62.181.91:3128','170.247.159.142:80','168.181.87.70:8080','171.5.163.196:8080','178.128.113.176:8080','178.128.93.230:8080','51.79.52.62:8080','46.209.131.244:8080','51.158.180.179:8811','52.140.242.103:3128','47.91.217.100:80','5.58.58.209:8080','51.158.98.121:8811','60.251.40.84:1080','59.152.103.106:8080','61.8.78.130:8080','83.175.166.234:8080','83.174.156.40:3128','81.95.230.211:3128','88.255.217.164:8080','89.219.21.174:8080','91.126.239.175:8080','101.254.136.130:44','103.123.171.218:8','102.177.105.34:3128','103.111.55.58:3098','103.125.105.4:808']
mDIR = "resources/data_sets/uk/test/"
IP_ADDRESS = ["52.179.231.206", "96.96.33.133", "198.12.157.28", "96.113.176.101"]


''' For getting keys and symbols list for file
'''
def create_list_from_file( url):
    response = ""
    with open(url, "r") as file_input_stream:
        response = file_input_stream.read().splitlines()
    file_input_stream.close()
    return response


        


async def fetch_data_proxy( mUrl):
    request_string = mUrl  
    # Randomly generate through IP Proxies each call
    # Different IP's: Unique IP every single request
    try:
        proxy_index = random.randint(0, len(IP_ADDRESS) - 1)
        proxy = {"http": IP_ADDRESS[proxy_index], "https": IP_ADDRESS[proxy_index]}
        print("TEST:",proxy_index)
        response = requests.get(url = request_string,proxies =proxy)
        print("proxy:",IP_ADDRESS[proxy_index])
        if response:
            string_resource_object = io.StringIO(response.content.decode('utf-8'))
            url_to_write = mDir + symbol + ".csv"
            with open(url_to_write , 'w') as file_output_stream:
                string_resource_object.seek(0)
                file_output_stream.write(string_resource_object.getvalue())
            file_output_stream.close()
            string_resource_object.close()
        else:
            print("Potential Server or Network Issue")
    except:
        print("Proxy issue")
            


async def task_builder(symbols_list,keys):
    """
    Builds 100 - 250 request strings; with appropriate keys and adds to tasks
    Determine whether to wait after 100
    """
    tasks = []
    count = 1
    key_pointer = 0
    current_key = keys[key_pointer]
    for i in symbols_list:
        if count == 100:
            sleep(300)
        if count % 5 == 0:
            if key_pointer > len(keys) -1:
                # Reset to zero; and wait 5 minutes
                key_pointer = 0
                current_key = keys[key_pointer]
            else:
                key_pointer+=1
                current_key = keys[key_pointer]
        print( count, ") Request for ", i) # Test
        print("Current Key: ",current_key)
        miner = data_miner.DataMiner()
        url = miner.create_alphavantage_url(i, "full", current_key)
        print(url)
        tasks.append(asyncio.ensure_future(fetch_data_proxy(url)))
        count+=1
    await asyncio.gather(*tasks)




# 1. Strategy 1) 20 threads (for each key) network requests with it's own proxy; makes 5 requests then stops.
# 2. For each symbol, make an async request; after 5 change proxy and key 
# Add to task each symbols a sync request
def mine_universe_async():
    """Initiates the async task. All the handling and generation and setup.
    """  

    symbols_list = create_list_from_file("resources/data_sets/symbols_list/ftse250_symbols.txt")
    keys = create_list_from_file("resources/alpha_vantage_keys.txt")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_builder(symbols_list, keys))
    loop.close()

mine_universe_async()




