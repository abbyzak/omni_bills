from telethon import TelegramClient, events
import requests
#******************************************************************************************************
import requests

# CoinMarketCap API endpoint
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
API_KEY = 'a1f27215-8a1a-4864-ac93-ff48c3b34b1f'

# Configurable settings
percentage_change_threshold = 0.0
candle_count_threshold = 0
market_cap_threshold = 0

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
        coins = data['data']#,key=lambda x:x['self_reported_market_cap'],reverse=True)
        for i in coins :
            mkcp = i['quote']['USD']['market_cap']
            i['market_cap'] = mkcp

        coins = sorted(coins,key=lambda x:x['market_cap'],reverse=True)
        filtered_coins = []
        for coin in coins[0:500]:
            symbol = coin['symbol']
            price_change_1h = coin['quote']['USD']['percent_change_1h']
            total_supply = coin['total_supply']
            market_cap = coin['quote']['USD']['market_cap']

            if (
                price_change_1h >= percentage_change_threshold and
                total_supply is not None and total_supply >= candle_count_threshold and
                market_cap > market_cap_threshold
            ):
                filtered_coins.append({
                    'symbol': symbol,
                    'price_change_1h': price_change_1h,
                    'candle_count': total_supply,
                    'market_cap': market_cap
                })
        return filtered_coins

    else:
        print(f'Error: {response.status_code} - {response.text}')
        return []

def mass():
    filtered_coins = get_filtered_coins()
    b = []
    for coin in filtered_coins:
        symbol = coin['symbol']
        price_change_1h = coin['price_change_1h']
        candle_count = coin['candle_count']
        market_cap = coin['market_cap']
        
        b.append(f"Coin: {symbol} Percentage Change in 1H: {price_change_1h:.2f}% Candle Count: {candle_count} Market Cap: ${market_cap}\n")
    return b
def group_strings(strings, chunk_size):
    result = []
    for i in range(0, len(strings), chunk_size):
        chunk = strings[i:i+chunk_size]
        result.append(''.join(chunk))
    return result  


#******************************************************************************************************
# api_id and api_hash from https://my.telegram.org/apps
api_id = '28811360'
api_hash = '62df1732bba44f40f37bcdcbe78e22be'

client = TelegramClient('user', api_id, api_hash).start()

# This message can contain any text, links, and emoji:
@client.on(events.NewMessage())
async def handler(event):
    sender = await event.get_input_sender()
    for i in group_strings(mass(),10):
        await client.send_message(sender, i)
        break

client.run_until_disconnected()
