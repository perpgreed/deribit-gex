import aiohttp
import asyncio
from aiolimiter import AsyncLimiter

CURRENCY = 'BTC'
CONTRACT_SIZE = 1
limiter = AsyncLimiter(20, 1)

async def get_options(session):
    params = {'currency' : CURRENCY, 'kind' : 'option'}
    async with session.get('https://www.deribit.com/api/v2/public/get_instruments', params=params) as resp:
        data = await resp.json()
        return [i for i in data['result']]
    
async def get_ob(session, queue, results):
            while not queue.empty():
                i = await queue.get()
                await asyncio.sleep(0.05)
                try:
                    async with limiter:       
                        async with session.get('https://www.deribit.com/api/v2/public/get_order_book', params={'instrument_name' : i['instrument_name']}) as resp:
                            status = resp.status
                            print(f'{i['instrument_name']} | Status: {status}')
                            if status == 200:
                                data = await resp.json()
                                results.append((i, data))
                except Exception as e:
                     print(f'Error fetching {i['instrument_name']}: {e}')
                finally:
                     queue.task_done()                 

async def gex(options, session):
    queue = asyncio.Queue()
    results = []
    for i in options:
         await queue.put(i)
    workers = [asyncio.create_task(get_ob(session, queue, results)) for t in range(20)]
    await queue.join()
    for w in workers:
         w.cancel()

    spot, gex = None, {}

    for i, data in results:
        if spot is None:
            spot = data['result']['underlying_price']
        gamma = data['result']['greeks']['gamma']
        oi = data['result']['open_interest']
        sign = 1 if i['option_type'] == 'call' else -1
        strike = i['strike']
        gex[strike] = gex.get(strike, 0.0) + sign * gamma * oi * CONTRACT_SIZE

    net_total = sum(gex.values())
    abs_total = sum(abs(v) for v in gex.values())
    upper = max(((k, v) for k, v in gex.items() if k > spot), key=lambda x: abs(x[1]), default=(None, 0))
    lower = max(((k, v) for k, v in gex.items() if k < spot), key=lambda x: abs(x[1]), default=(None, 0))
    return spot, upper, lower, net_total, abs_total

async def main():
    async with aiohttp.ClientSession() as session:
        options = await get_options(session)
        spot, (strike_upper, gex_upper), (strike_lower, gex_lower), net_total, abs_total = await gex(options, session)
        print(f'Spot Price: {spot}\nmax GEX above: {strike_upper} | gamma*OI: {gex_upper:+.2f}\nmax GEX below: {strike_lower} | gamma*OI: {gex_lower:+.2f}\nnet total GEX: {net_total:+.2f}\nabsolute total GEX: {abs_total:+.2f}')

if __name__ == '__main__':
    asyncio.run(main())