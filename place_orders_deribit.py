# Import the library
import deribit_api

# Initialize the client and set it to use the testnet
deribit_api_client = deribit_api.Client(test=True)

# Authenticate using your testnet API key
deribit_api_client.auth(client_id='your_testnet_client_id', secret='your_testnet_secret_key')

# Define the order details
instrument = 'BTC-PERPETUAL'  # the instrument you want to trade
quantity = 1.0  # the quantity of the instrument you want to buy/sell
price = 10000.0  # the price you want to buy/sell at
order_type = 'limit'  # the type of order (can be 'limit' or 'market')
side = 'buy'  # the side of the trade (can be 'buy' or 'sell')

# Place the order
response = deribit_api_client.place_order(instrument=instrument, quantity=quantity, price=price, order_type=order_type, side=side)

# Print the order details
print(response)
