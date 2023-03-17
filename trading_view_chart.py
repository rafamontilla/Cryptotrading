import asyncio
import json
import websockets
import pandas as pd
import mplfinance as mpf

async def get_chart_data(instrument_name, start_timestamp, end_timestamp, resolution):
    # Assemble the JSON message with the method parameters
    msg = {
        "jsonrpc": "2.0",
        "id": 833,
        "method": "public/get_tradingview_chart_data",
        "params": {
            "instrument_name": instrument_name,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "resolution": resolution
        }
    }

    # Establish WebSocket connection to Deribit API endpoint
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        # Sends the JSON message to Deribit
        await websocket.send(json.dumps(msg))

        while websocket.open:
            # Receives response from Deribit
            response_json = await websocket.recv()
            response_dict = json.loads(response_json)

            # Extract the necessary columns from the 'result' object
            df = pd.DataFrame(response_dict['result'], columns=['open', 'close', 'high', 'low', 'volume', 'ticks'])

            # Convert the 'ticks' column from milliseconds to a datetime format
            df['ticks'] = pd.to_datetime(df['ticks'], unit='ms')

            # Create the candlestick chart using mplfinance
            mpf.plot(df.set_index('ticks'), type='candle')

# Example usage
instrument_name = "BTC-PERPETUAL"
start_timestamp = 1647360000000  # 15/03/2022
end_timestamp = 1678896000000  # 15/03/2023
resolution = "30"  # 30 minutes

asyncio.get_event_loop().run_until_complete(get_chart_data(instrument_name, start_timestamp, end_timestamp, resolution))
