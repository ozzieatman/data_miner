
"""data_miner.py file holds the DataMiner class. 
The class handles network requests to a url and saves responses as CSVs.
Class also ask convinient wrapper methods for creating queries to IEX and Alpha Vantage
"""


#Imports
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import shutil



class DataMiner:
    """
    READ ME: How to Mine data from IEX and Alpha Vantage and store as a CSV
    0) Import
    1) Enter your keys
    2) Create a new Data Miner Object and use alpha_vantage_source or iex_source to build a URL
    3) Call fetch data method

        EXAMPLE:

        from minning.data_miner import DataMiner

        miner = DataMiner()
        miner.set_UK(True)
        query = miner.create_alphavantage_url("IBM", "full", DataMiner.ALPHA_VANTAGE_KEY)
        miner.fetch_data(query)
    """
    # CONSTANTS: Make sure you add your personal keys.
    ALPHA_VANTAGE_KEY = "ENTER_KEY_HERE" 
    IEX_KEY = "ENTER_KEY_HERE"


    def __init__(self):
        self.key = ""
        self.is_uk = False
        self.mDir = ""

    def set_key(self, key):
        """ Used for dynamically resetting the key during runtime""; intended for use with subclassess
        key - string value or parsed list
        """
        self.key = key

    def set_dir(self, mDir):
        """Sets the directory you want to download CSV's to. 
        mDir - string directory.
        """
        self.mDir = mDir

    def set_UK(self,is_uk):
        """ If UK will automaticall append .LON for alpha_vantage create_url
        is_uk - boolean True / False
        """ 
        self.is_uk = is_uk


        

    def create_alphavantage_url(self, symbol, outputsize, key_ ):
        """ Convinience method for creating Alpha Vantage Queries 
        @Params: 
        symbol -  ie: AAPL type string. 
        outputsize -  compact / full. Last 100 data points of last 20 years.
        key_ - use dynamic key or ALPHA_VANTAGE_KEY constant

        @Returns:
        Returns string url query.  
        """
        if self.is_uk == True:
            symbol = symbol + ".LON"
        source = "https://www.alphavantage.co/query/?"
        function_to_call = "function=TIME_SERIES_DAILY" 
        mSymbol = "&symbol=" + symbol
        mOutputsize = "&outputsize=" + outputsize
        datatype = "&datatype=csv"
        key = "&apikey=" + key_
        self.symbol = symbol
        self.url = source + function_to_call + mSymbol  + datatype  + mOutputsize +key
        return self.url

    def create_iex_url(self, symbol):
        """ 
        GET /stock/{symbol}/chart/{range}/{date}
        Builds the URL for IEX Data Provider
        @Params: symbol ie: AAPL
        """
        iex_source = "https://cloud.iexapis.com/"
        version = "v1/"
        endpoint = "stock/" + symbol + "/chart" + "/1m"
        self.set_key(self.IEX_KEY)
        query =  "?format=csv&token=" +self.key

        self.url = source + version + endpoint + query
        return self.url

    def write_to_csv(self, url, mObject):
        """Private Method that handles write to disk.
        @Params: 
        url - the mDir location to write to file
        mObject - the object to write"""
        with open(url , 'w') as file_output_stream:
            mObject.seek(0)
            file_output_stream.write(mObject.getvalue())
        file_output_stream.close()
        mObject.close()


    def fetch_data(self, query_url):
        """Handles the network request.
        @Params: the query url
        """
        # Concatenation
        request_string = query_url 
        # TODO Should we Try / Catch here
        response = requests.get(url = request_string) 
        if response:
            string_resource_object = io.StringIO(response.content.decode('utf-8'))
            url = self.mDir + self.symbol + ".csv"
            self.write_to_csv(url, string_resource_object)
        else: 
            print ("Problem with request")