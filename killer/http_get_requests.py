import sys
import asyncio
import aiohttp
import time


async def send_request(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return True
            else:
                return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False


async def send_requests(url, req_per_sec):
    async with aiohttp.ClientSession() as session:
        while True:
            start_time = time.time()
            tasks = []

            for _ in range(req_per_sec):
                tasks.append(send_request(session, url))

            results = await asyncio.gather(*tasks)
            requests_sent = sum(1 for result in results if result)

            print(f"Requests sent in 1 second: {requests_sent}")
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1 - elapsed_time)
            await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 http_get_requests.py <URL> <Requests per second>")
        print("Using default values: URL = http://10.141.10.72:30003/swagger/#/default/get__user_id__hives/index.html, Requests per second = 10")
        url = "http://10.141.10.72:30003/swagger/#/default/get__user_id__hives/index.html"
        req_per_sec = 10
    else:
        url = sys.argv[1]
        req_per_sec = int(sys.argv[2])

    asyncio.run(send_requests(url, req_per_sec))
