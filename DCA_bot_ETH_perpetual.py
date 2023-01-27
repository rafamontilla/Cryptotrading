import deribit_api
import pandas as pd

# Initialize the client and set it to use the testnet
deribit_api_client = deribit_api.Client(test=True)

# Authenticate using your testnet API key
deribit_api_client.auth(client_id='your_testnet_client_id', secret='your_testnet_secret_key')

# Define the parameters for your bot
interval = '1d'  # the interval at which to buy
budget = 1000  # the total budget for buying ETH

while True:
    # Retrieve the historical price data for ETH
    historical_data = deribit_api_client.get_tradingview_data(instrument='ETH-PERPETUAL', resolution=interval)
    df = pd.DataFrame(historical_data['data'], columns=historical_data['columns'])

    # Calculate the moving average for the last 50 data points
    ma_50 = df['close'].tail(50).mean()

    # Retrieve the current price of ETH
    ticker = deribit_api_client.get_instrument('ETH-PERPETUAL')
    current_price = ticker['last_price']

    # Calculate the number of ETH that can be bought with the budget
    eth_units = budget / current_price

    # Check if the current price is below the moving average and if budget allows to buy
    if current_price < ma_50 and budget >= current_price:
        # Place the buy order
        response = deribit_api_client.place_order(instrument='ETH-PERPETUAL', quantity=eth_units, price=current_price, order_type='market', side='buy')
        print(f'Bought {eth_units} ETH at {current_price}')
        # Update the budget
        budget -= current_price * eth_units
    else:
        print(f'Price {current_price} is above the moving average {ma_50} or budget is not enough')

    # Sleep for the defined interval before checking again
    time.sleep(60 * 60 * 24) # sleep for 24 hours
