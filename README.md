# data_miner
Synchronous Data Miner for IEX and Alpha Vantage 

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
