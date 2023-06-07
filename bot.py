import requests
from datetime import datetime, timedelta
from telethon import TelegramClient, events
# CoinMarketCap API endpoints
LISTINGS_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
HISTORICAL_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/latest'

# Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
API_KEY = 'a1f27215-8a1a-4864-ac93-ff48c3b34b1f'

# Configurable settings
percentage_change_threshold = 0.0
market_cap_threshold = 0
candle_count_threshold = 1  # Minimum number of candles within the last hour


def get_filtered_coins():
    # Make API request to CoinMarketCap
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    params = {
        'start': '1',
        'limit': '500',
        'convert': 'USD'
    }
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        coins = data['data']
        for i in coins:
            mkcp = i['quote']['USD']['market_cap']
            i['market_cap'] = mkcp

        coins = sorted(coins, key=lambda x: x['market_cap'], reverse=True)
        filtered_coins = []
        for coin in coins[0:500]:
            symbol = coin['symbol']
            price_change_1h = coin['quote']['USD']['percent_change_1h']
            price_change_24h = coin['quote']['USD']['percent_change_24h']
            total_supply = coin['total_supply']
            market_cap = coin['quote']['USD']['market_cap']

            # Ensure candle count is within the range of 1 to 100
            candle_count = min(max(int(total_supply / 100000000), 1), 100)

            # Calculate the 4-hour percentage change
            price_change_4h = ((1 + price_change_24h / 100) ** (1 / 6) - 1) * 100

            if (
                price_change_1h >= percentage_change_threshold and
                price_change_4h >= percentage_change_threshold and
                price_change_24h >= percentage_change_threshold and
                market_cap > market_cap_threshold
            ):
                filtered_coins.append({
                    'symbol': symbol,
                    'price_change_1h': price_change_1h,
                    'price_change_4h': price_change_4h,
                    'price_change_24h': price_change_24h,
                    'candle_count': candle_count,
                    'market_cap': market_cap
                })
        return filtered_coins

    else:
        print(f'Error: {response.status_code} - {response.text}')
        return []

def main(interval='01h'):
    filtered_coins = get_filtered_coins()

    for coin in filtered_coins:
        symbol = coin['symbol']
        price_change_1h = coin['price_change_1h']
        price_change_4h = coin['price_change_4h']
        price_change_24h = coin['price_change_24h']
        candle_count = coin['candle_count']
        market_cap = coin['market_cap']
        b = []
        if interval == '01h':
            b.append(f"Coin: {symbol} Percentage Change in 1H: {price_change_1h:.2f}% Candle Count: {candle_count*int(interval[0:2])} Market Cap: ${market_cap / 1_000_000:.2f} mil\n")
        if interval == '04h':
            b.append(f"Coin: {symbol} Percentage Change in 4H: {price_change_4h:.2f}% Candle Count: {candle_count*int(interval[0:2])} Market Cap: ${market_cap / 1_000_000:.2f} mil\n")
        if interval == '24h':
            b.append(f"Coin: {symbol} Percentage Change in 24H: {price_change_24h:.2f}% Candle Count: {candle_count*int(interval[0:2])} Market Cap: ${market_cap / 1_000_000:.2f} mil\n")
        print(f"Market Cap: {market_cap / 1_000_000:.2f} mil $")

def group_strings(strings, chunk_size):
    result = []
    for i in range(0, len(strings), chunk_size):
        chunk = strings[i:i+chunk_size]
        result.append(''.join(chunk))
    return result

# api_id and api_hash from https://my.telegram.org/apps
api_id = '28811360'
api_hash = '62df1732bba44f40f37bcdcbe78e22be'

client = TelegramClient('user', api_id, api_hash).start()

# This message can contain any text, links, and emoji:
@client.on(events.NewMessage())
async def handler(event):
    sender = await event.get_input_sender()
    message = event.message.message.lower()  # Convert the message to lowercase for easier comparison

    if '1h' in message:
        for i in group_strings(main(), 10):
            await client.send_message(sender, i)
            break
    elif '4h' in message:
        for i in group_strings(main('4h'), 10):
            await client.send_message(sender, i)
            break
    elif '24h' in message:
        for i in group_strings(main('24h'), 10):
            await client.send_message(sender, i)
            break
    else:
        predictions = []
    
client.run_until_disconnected()

