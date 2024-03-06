# import functions
import requests
import json
import sys

# api key
api_key = input("Enter Authenticated KAIKO API Key: ")

# choice of data to download
choice = int(input("To download data: \n Enter 1 for EXCHANGE DATA \n Enter 2 for OHLCV DATA \n Enter 3 for ORDER BOOK DATA \n"))
if choice == 1:
    # URL with Start and End time provided by user - must follow format in order to work
    print("**Data MUST be within the past 3 years**")
    print("Start and End Times are in UTC (Coordinated Universal Time): The Standard Time Reference Used Worldwide")
    start_time = input("Enter the Start Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    end_time = input("Enter the End Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    url_choice = f'https://us.market-api.kaiko.io/v2/data/trades.v1/exchanges/cbse/spot/btc-usd/trades?start_time={start_time}&end_time={end_time}'
    # saves data to csv
    FILE_PATH = './EXCHANGE_DATA.csv'
elif choice == 2:
    # URL with Start and End time provided by user - must follow format in order to work
    print("**Data MUST be within the past 3 years**")
    print("Start and End Times are in UTC (Coordinated Universal Time): The Standard Time Reference Used Worldwide")
    start_time = input("Enter the Start Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    end_time = input("Enter the End Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    url_choice = f'https://us.market-api.kaiko.io/v2/data/trades.v1/exchanges/cbse/spot/btc-usd/aggregations/ohlcv?interval=1d&start_time={start_time}&end_time={end_time}&page_size=10'
    # saves data to csv
    FILE_PATH = './OHLCV_DATA.csv'
elif choice == 3:
    # URL with Start and End time provided by user - must follow format in order to work
    print("**Data MUST be within the past 1 month**")
    print("Start and End Times are in UTC (Coordinated Universal Time): The Standard Time Reference Used Worldwide")
    start_time = input("Enter the Start Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    end_time = input("Enter the End Time (MUST follow the format YYYY-MM-DDTHH:MM:SSZ): ")
    url_choice = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/krkn/spot/btc-usd/snapshots/full?start_time={start_time}&end_time={end_time}&slippage=0&page_size=10&limit_orders=10&slippage_ref=mid_price'
    # saves data to csv
    FILE_PATH = './ORDER_BOOK_DATA.csv'

# function to download data based on URL
def download_data(url: str = url_choice):
    try:
        with requests.Session() as session_instance:
            with session_instance.request(method='GET', url=url, headers={'X-Api-Key':api_key}) as http_response:
                response_content = json.loads(http_response.content)
                response_data_page = response_content['data']
                headers = ','.join(response_data_page[0].keys())
                with open(FILE_PATH, 'w') as fp:
                    fp.write(headers + '\n')
                for trade_record in response_data_page:
                    line = ','.join([str(val) for val in trade_record.values()])
                    with open(FILE_PATH, 'a') as fp:
                        fp.write(line + '\n')
                while 'next_url' in response_content:
                    with session_instance.request(method = 'GET', url=response_content['next_url'], headers={'X-Api-Key':api_key}) as next_response:
                        response_content = json.loads(next_response.content)
                        response_data_page = response_content['data']
                        for trade_record in response_data_page:
                            line = ','.join([str(val) for val in trade_record.values()])
                            with open(FILE_PATH, 'a') as fp:
                                fp.write(line + '\n')
        print("CSV is Saved to the Same Folder as this Python Script")
    except:
        print("ERROR: CHECK Authenticated KAIKO API Key OR Formatting of Start and End Time")

# runs script
if __name__ == '__main__':
    if len(sys.argv)> 1:
        user_provided_url = sys.argv[1]
        download_data(user_provided_url)
    else:
        download_data()
