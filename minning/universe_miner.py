
""" Universe Miner is built ontop of data miner and used for mining multiple CSV's"""
#Imports
import requests
import pandas as pd
import random
import io
import matplotlib.pyplot as plt
import shutil
from minning.data_miner import DataMiner
import minning.data_cleaner as cleaner
import time


class UniverseMiner(DataMiner):
    """ Example how how to use:
    1) Import 
    2) Add key into DataMiner
    3) Use the mine_univer_on_timer, if using a single key.
    4) Use the mine_universe_on_intervals if using multiple keys
    
    Example:
    from minning.universe_minner import UniverseMiner

    universe_miner = UniverseMiner(symbols_="ftse100_symbols.txt", keys="alpha_vantage_keys.txt",dst_dir="data_sets/uk/ftse100/")
    universe_miner.set_UK(True)
    universe_miner.mine_universe_on_timer_with_intervals()

    OR 

    universe_miner = UniverseMiner(symbols_="ftse100_symbols.txt", keys="default",dst_dir="data_sets/uk/ftse100/")
    universe_miner.set_UK(True)
    universe_miner.mine_universe_on_timer()

    """
    # Constants
    IP_ADDRESS = ['140.82.59.209:8080','159.8.114.37:8123','159.138.1.185:80','159.138.1.185:443','159.89.128.93:8080','159.203.44.177:3128','165.98.139.26:8080','168.131.152.107:3128','169.62.181.91:3128','170.247.159.142:80','168.181.87.70:8080','171.5.163.196:8080','178.128.113.176:8080','178.128.93.230:8080','51.79.52.62:8080','46.209.131.244:8080','51.158.180.179:8811','52.140.242.103:3128','47.91.217.100:80','5.58.58.209:8080','51.158.98.121:8811','60.251.40.84:1080','59.152.103.106:8080','61.8.78.130:8080','83.175.166.234:8080','83.174.156.40:3128','81.95.230.211:3128','88.255.217.164:8080','89.219.21.174:8080','91.126.239.175:8080','101.254.136.130:44','103.123.171.218:8','102.177.105.34:3128','103.111.55.58:3098','103.125.105.4:808']
    def __init__(self, symbols_, keys , dst_dir):
        """@Params:
        symbols_ - a list of symbols of an index ie: ftse100 in a txt file
        keys - a file with a list of keys ie: keys.txt or default
        dst_dir - the destination for saving all CSV's 
        """
        super().__init__()
        self.symbols_list = cleaner.clean_white_spaces((self.create_list_from_file(symbols_)))
        if keys != "default":
            self.keys = cleaner.clean_white_spaces(self.create_list_from_file(keys))
        self.mDir = dst_dir
        self.proxy_list = ""
    

    def set_proxy(self, proxy_list):
        """Takes a list of strings"""
        self.proxy_list = proxy_list


    def use_default_proxies(self):
        """For usage with the mine_universe_on_proxy
        Takes a boolean True or False
        """
        self.proxy_list = self.IP_ADDRESS

    
    def create_list_from_file(self, url):
        """Utility helper function that reads from a file; takes destination url and returns a list of strings"""
        response = ""
        with open(url, "r") as file_input_stream:
            response = file_input_stream.read().splitlines()
        file_input_stream.close()
        return response
    

    def fetch_data_proxy(self, url):
        """Private method, not to be called outside Class. This will be used by the mine_universe_proxy_on_proxy exclusive"""
        request_string = url  
        # Randomly generate through IP Proxies each call
        # Different IP's: Unique IP every single request
        try:
            proxy_index = random.randint(0, len(self.ip_addresses) - 1)
            proxy = {"http": self.ip_addresses[proxy_index], "https": self.ip_addresses[proxy_index]}
            print("TEST:",proxy_index)
            response = requests.get(url = request_string,proxies =proxy)
            print("proxy:",self.ip_addresses[proxy_index])
            if response:
                string_resource_object = io.StringIO(response.content.decode('utf-8'))
                url = self.mDir + self.symbol + ".csv"
                self.write_to_csv(url, string_resource_object)
            else:
                print("Potential Server or Network Issue")
        except:
            print("Proxy Issue here")
            
        

    # 2. Strategy 2) Timer; waits 5 minutes
    def mine_universe_on_timer(self):  
        """Current limitation is only 5 requests per 1 minutes
        @NOTE Only use if using single key: or keys set to default
        """
        count = 1
        for i in self.symbols_list:
            if count % 5 == 0:
                time.sleep(61)
            print( count, ") Request for ", i) # Test
            url = self.create_alphavantage_url(i, "full", self.ALPHA_VANTAGE_KEY)
            self.fetch_data(url)
            count+=1

    #Iterate through keys; wait 10 seconds every 5 requests 
    def mine_universe_on_timer_with_intervals(self):  
        """Mines universe using multiple keys. @NOTE only using if using multiple keys
        """
        count = 1
        key_pointer = 0
        current_key = self.keys[key_pointer]
        for i in self.symbols_list:
            if count % 5 == 0:
                key_pointer+=1
                current_key = self.keys[key_pointer]
                time.sleep(61)
            elif key_pointer >= len(self.keys) -1:
                # Reset to zero; and wait 5 minutes
                key_pointer = 0
                print(f"KEY POINTER: {key_pointer} ")
                print("Length of keys: ", len(self.keys))
                current_key = self.keys[key_pointer]
                time.sleep(61)
            print(f"KEY: {current_key} \n  {count}) Request for ", i) # Test
            url = self.create_alphavantage_url(i, "full", current_key)
            self.fetch_data(url)
            count+=1



    def mine_universe_on_proxy(self):
        """Mine Universe using proxies; only use if using good proxies. This is ideally also used with multi - threads. See async_universe_miner_script
        @NOTE: In current state this is very inefficient unless using very fast proxies.
        
        @TODO Could consider sequentially using keys and proxies; after 5 requests switch proxy and key.
        In this instance we are doing it random; where in request is a random key and random proxy.
        We are making the assumption that there is no notable speed difference.
        """
        count = 0
        for i in self.universe_list:
            if self.is_uk:
                i = i + ".LON"
            if count % 5 == 0:
                print("Count:", count)
                # Iterate through the keys
                self.key_pointer+=1
                if self.key_pointer == len(self.keys) -1:
                    self.key_pointer = 0
                latest_key = self.keys[self.key_pointer]
                print(latest_key) #T
                self.universe_miner.set_key(latest_key)                
            count+=1
            print( count, ") Request for ", i) # Test
            self.universe_miner.create_alphavantage_url(i, "full")
            print(self.universe_miner.url)
            self.universe_miner.fetch_data_proxy()





