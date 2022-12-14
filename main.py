import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup as bs
from os import system, path, mkdir, getcwd
import requests

start_time = time.time()
all_data = []
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28',  '29', '30', '31']
# months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months = ['10', '11', '12']

class cs:
    INFO = '\033[93m'
    GREEN = '\033[92m'
    END = '\033[0m'



async def downloads_photo(session, url, title, day, month, offset, photos):
    async with session.get(url) as resp:
        print(url)
        if resp.status != 200:
            print(f'resp.status: {resp.status}')
        else:
            for i in range(len(photos)):
                content = await resp.read()
                with open(f"images/{title}/{day}_{month}_{offset}/{month}_{day}_{offset}_{i}.jpg", "wb") as file:
                    file.write(content)
        return




async def get_page_data(session, title: str, month: int, day: int, offset: int=None) -> str:
    if offset:
        url = f'https://telegra.ph/{title}-{month}-{day}-{offset}'
    else:
        offset = ''
        url = f'https://telegra.ph/{title}-{month}-{day}'
    async with session.get(url) as resp:
        if resp.status != 200:
            return
        else:
            with open('valid_urls.txt', "a+") as file:
                file.write(f'{url}\n')
            content = await resp.read()
            resp_text = await resp.text()
            soup = bs(resp_text, 'html.parser')
            items = soup.findAll('img')
            photos = []
            for item in items:
                src = item.get('src')
                if not "http" in src:
                    photos.append(f"https://telegra.ph{src}")
            if photos:
                if not path.isdir(f"{getcwd()}\\images"):
                    mkdir(f"{getcwd()}\\images")
                if not path.isdir(f"{getcwd()}\\images\\{title}"):
                    mkdir(f"{getcwd()}\\images\\{title}")
                if not path.isdir(f"{getcwd()}\\images\\{title}\\{day}_{month}_{offset}"):
                    mkdir(f"{getcwd()}\\images\\{title}\\{day}_{month}_{offset}")
                with open(f"images/{title}/{day}_{month}_{offset}/{month}_{day}_{offset}.html", "wb") as file:
                    file.write(content)
                tasks_2 = []
                for i in range(len(photos)):
                    task_2 = asyncio.create_task(downloads_photo(session, photos[i], title, day, month, offset, photos))
                    tasks_2.append(task_2)
                await asyncio.gather(*tasks_2)



async def load_site_data(offset: int=None):
    # titles = ['alina-nikitina', 'sliv-shemy', 'nikitina']
    titles = ['sliv-byvshej']
    async with aiohttp.ClientSession() as session:
        tasks = []
        for title in titles:
            for month in months:
                for day in days:
                    task = asyncio.create_task(get_page_data(session, title, month, day))
                    tasks.append(task)
                    for offset in range(1, int(offset) + 1):
                        task = asyncio.create_task(get_page_data(session, title, month, day, offset))
                        tasks.append(task)
        await asyncio.gather(*tasks)



if __name__ == '__main__':
    try:
        asyncio.run(load_site_data(offset=10))
        end_time = time.time() - start_time
        print(f"\nExecution time: {end_time} seconds")
    except Exception as e:
        print(e)
