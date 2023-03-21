import asyncio
import json
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import pytz
import time
import websockets

# Defines the request information
instrument_name = 'BTC-PERPETUAL'
start_timestamp = 0
resolution = 10

fig = go.Figure()

msg = {
  'jsonrpc': '2.0',
  'id': 833,
  'method': 'public/get_tradingview_chart_data',
  'params': {
    'instrument_name': instrument_name,
    'start_timestamp': start_timestamp,
    'end_timestamp': int(time.time()) * 1000,
    'resolution': resolution
  }
}

# Defines the function that receives and processes the response from Deribit
async def process_response(response):
    response = json.loads(response)
    if 'result' in response:
        data = response['result']
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['ticks'], unit='ms')
        df['time'] = df['time'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
        fig.add_trace(go.Candlestick(x=df['time'],
                                      open=df['open'],
                                      high=df['high'],
                                      low=df['low'],
                                      close=df['close']))
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.show()
        
        # updates the value of start_timestamp and end_timestamp before making a new request
        start_timestamp = int(df['ticks'].iloc[-1]) + 1
        end_timestamp = int(time.time()) * 1000
        msg['params']['start_timestamp'] = start_timestamp
        msg['params']['end_timestamp'] = end_timestamp
        
    await asyncio.sleep(10)
    await call_api(msg)

# Define the function that makes the request to Deribit
async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        await websocket.send(json.dumps(msg))
        while websocket.open:
            response = await websocket.recv()
            await process_response(response)

# Start the request
asyncio.get_event_loop().run_until_complete(call_api(msg))
