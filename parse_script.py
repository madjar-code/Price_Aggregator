import time
import requests
from typing import Iterable, Optional
from pydantic import HttpUrl
from concurrent.futures import ThreadPoolExecutor
from decorators import measure_time


urls: Iterable[HttpUrl] = [
    'https://linella.md/',
    'https://nr1.md/',
]


@measure_time
def fetch_price(url: HttpUrl) -> Optional[int]:
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        error_str: str = str(e)[:100] + '...'\
            if len(str(e)) > 100 else str(e)
        error_message = f'Error fetching {url}: {error_str}'
        print(error_message)
    except Exception as e:
        error_message = f'Something went wrong: {e}'
        print(error_message)


def main():
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(fetch_price, urls)
        for result in results:
            print(result)
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"Total execution time: {total_duration:.2f} seconds")


if __name__ == '__main__':
    main()
