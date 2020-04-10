#Imports
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import shutil



class DataMiner:
    """
    READ ME: How to Mine data from IEX and Alpha Vantage and store as a CSV

    0) Enter your keys

    1) Create a new Data Miner Object and use alpha_vantage_source or iex_source

    2) Use the create alpha_vantage_url or create iex_url functions; input your desired symbols

    3) Call fetch data method

        EXAMPLE:

        miner = DataMiner(DataMiner.alpha_vantage_source)
        miner.create_alpha_vantage_url("IBM", "compact")
        miner.fetch_data()


    """

    # CONSTANTS:

    alpha_vantage_key = "YOUR_KEY_HERE" 
    alpha_vantage_source = "https://www.alphavantage.co/query/?"

    iex_key = "YOUR_KEY_HERE"
    iex_source = "https://cloud.iexapis.com/"
    ''

    """ The Directory you want to write CSV's to. Leave blank for current dir."""
    mDir = ""



    def __init__(self, source):
        self.source = source


        

    def create_alphavantage_url(self, symbol, outputsize ):
        ''' 
        Builds the URL for Alpha Vantage Data Provider
        @Params: symbol ie: AAPL, outputsize: compact / full
        '''
        function_to_call = "function=TIME_SERIES_DAILY"  
        mSymbol = "&symbol=" + symbol
        mOutputsize = "&outputsize=" + outputsize
        datatype = "&datatype=csv"
        key = "&apikey=" + self.alpha_vantage_key

        self.symbol = symbol


        self.url = self.source + function_to_call + mSymbol  + datatype  + mOutputsize +key
        return self.url

    def create_iex_url(self, symbol):
        ''' 
        'GET /stock/{symbol}/chart/{range}/{date}'
        Builds the URL for IEX Data Provider
        @Params: symbol ie: AAPL
        '''
        version = "v1/"
        endpoint = "stock/" + symbol + "/chart" + "/1m"
        query =  "?format=csv&token=" +self.iex_key

        self.url = self.source + version + endpoint + query
        return self.url

    ''' PRIVATE Method '''
    def write_to_csv(self, url, mObject):
        with open(url , 'w') as file_output_stream:
            mObject.seek(0)
            file_output_stream.write(mObject.getvalue())
        file_output_stream.close()
        mObject.close()


    ''' PRIVATE Method '''
    def fetch_data(self):
        # Concatenation
        request_string = self.url  
        # TODO Should we Try / Catch here
        response = requests.get(url = request_string) 
        if response:
            string_resource_object = io.StringIO(response.content.decode('utf-8'))
            url = self.mDir + self.symbol + ".csv"
            self.write_to_csv(url, string_resource_object)
        else: 
            print ("Problem with request")