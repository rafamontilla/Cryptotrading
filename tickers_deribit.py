import requests
import csv

# Open a CSV file to write the ticker data
with open('tickers.csv', mode='w') as csv_file:
    fieldnames = ['instrument_name', 'currency']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # Make the API request to get the list of BTC instruments
    response = requests.get("https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&expired=false")
    data = response.json()['result']

    # Iterate over the BTC instruments
    for instrument in data:
        # Write the instrument information to the CSV file
        writer.writerow({'instrument_name':instrument['instrument_name'], 'currency': 'BTC'})

    # Make the API request to get the list of ETH instruments
    response = requests.get("https://www.deribit.com/api/v2/public/get_instruments?currency=ETH&expired=false")
    data = response.json()['result']

    # Iterate over the ETH instruments
    for instrument in data:
        # Write the instrument information to the CSV file
        writer.writerow({'instrument_name':instrument['instrument_name'], 'currency': 'ETH'})
